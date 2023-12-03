function doGet() {
    var htmlTemplate = HtmlService.createTemplateFromFile('Page');
    return htmlTemplate.evaluate();
}

function getTasks() {
    var tasks = [];
    var taskLists = Tasks.Tasklists.list();
    if (taskLists.items) {
        for (var i = 0; i < taskLists.items.length; i++) {
            var taskList = taskLists.items[i];
            var tasksInList = Tasks.Tasks.list(taskList.id);
            if (tasksInList.items) {
                tasks = tasks.concat(tasksInList.items);
            }
        }
    }
    return tasks;
}

function predictDuration(task) {
    var parts = task.title.split("-");
    if (parts.length !== 3) return null; // Ensure the format is correct

    var subject = parts[0];
    var problems = parseInt(parts[1]);
    var priority = parts[2];

    var data = {
        "Subject": subject,
        "Problem Set": problems,
        "Priority": priority
    };

    var options = {
        'method': 'post',
        'contentType': 'application/json',
        'payload': JSON.stringify(data)
    };

    var response = UrlFetchApp.fetch('HEROKU_API_URL', options);
    var prediction = JSON.parse(response.getContentText());
    var duration = parseFloat(prediction[0]); // Convert string to a floating-point number // Assuming the prediction is a single value

     // Log the original prediction
    Logger.log("Original prediction: " + duration + " For subject" + subject);

    // Adjust the duration based on the conditions
    if (duration < 0) {
        duration = -duration; // Make the duration positive
    }
    if (duration < 50) {
        duration += Math.random() * (100); // Add random value to make it at least 50
    }
    duration = Math.min(duration, 420); // Cap the duration at 420

    // Log the final duration
    Logger.log("Adjusted duration: " + duration + "For subject" + subject);

    return duration; // Assuming the prediction is a single value
}

function scheduleTasks() {
    var tasks = getTasks();
    var calendar = CalendarApp.getDefaultCalendar();
    var scheduledTasks = []; // Array to store scheduled tasks info
    var maxDaysAhead = 7; // Define how many days ahead you want to check
    var maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + maxDaysAhead); // Set the maximum date to check

    tasks.forEach(function(task) {
        var duration = predictDuration(task);
        if (!duration || duration <= 0) {
            Logger.log("Invalid duration for task: " + task.title);
            Logger.log("Duration: " + duration);
            return; // Skip this task if duration is invalid
        }
        var taskDetails = parseTaskDetails(task.title);
        if (!taskDetails) return; // Skip if task details are not properly formatted

        var start = getNextStartTime(new Date()); // Get the next 9 AM
        var end = new Date(start.getTime() + duration * 60000); // Add duration to start time
        Logger.log("Start Time: " + start);
        Logger.log("End Time: " + end);
        Logger.log("Duration: " + duration);

        while (!isValidTimeSlot(calendar, start, end)) {
            if (start > maxDate) {
                Logger.log("Could not find a slot for task: " + task.title);
                return; // Skip this task if no slot found within max days ahead
            }
            start = getNextStartTime(new Date(start.getTime() + 60 * 60000)); // Move to the next hour or next day
            end = new Date(start.getTime() + duration * 60000);
        }

        var eventTitle = "Finish " + taskDetails.problems + " problems for " + taskDetails.subject + " (" + taskDetails.priority + " priority)";
        // Create the event
        calendar.createEvent(eventTitle, start, end);
        // Push an object with title and time to the array
        scheduledTasks.push({
            title: eventTitle,
            time: start.toLocaleString() + " to " + end.toLocaleString()
        });
    });
    return scheduledTasks;
}

function parseTaskDetails(taskTitle) {
    var parts = taskTitle.split("-");
    if (parts.length !== 3) return null;

    return {
        subject: parts[0],
        problems: parts[1],
        priority: parts[2]
    };
}

function getNextStartTime(date) {
    var nextStart = new Date(date.getTime());
    nextStart.setMinutes(0);
    nextStart.setSeconds(0);
    nextStart.setMilliseconds(0);

    // If it's before 9 AM, start at 9 AM
    if (nextStart.getHours() < 9) {
        nextStart.setHours(9);
    } 
    // If it's after 5 PM, move to 9 AM next day
    else if (nextStart.getHours() >= 17) {
        nextStart.setDate(nextStart.getDate() + 1);
        nextStart.setHours(9);
    }
    // If it's during the day, move to the next hour
    else {
        nextStart.setHours(nextStart.getHours() + 1);
    }

    return nextStart;
}

function isValidTimeSlot(calendar, start, end) {
    // Ensure end is after start
    if (end <= start) {
        return false;
    }
    var events = calendar.getEvents(start, end);
    return events.length === 0 && start.getDay() != 0 && start.getDay() != 6; // Check if slot is free and not on weekend
}



