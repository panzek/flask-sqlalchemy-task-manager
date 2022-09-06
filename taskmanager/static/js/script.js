// initialize the sidenav plugin, initialization code copied from Materialize and edited
document.addEventListener('DOMContentLoaded', function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav'); // The querySelector will be 'sidenav'
    M.Sidenav.init(sidenav); // we initialize that without defining any variable

    // datepicker initialization
    let datepicker = document.querySelectorAll(".datepicker");
    M.Datepicker.init(datepicker, {
        format: "dd mmmm, yyyy",
        i18n: {done: "Select"}
    });
/*
On Materialize Dat Picker page:
First, we make sure that all tasks have a consistent date format, which uses the 'format' key.
For this project, I'm going to specify the date format of "dd mmmm, yyyy", which would be for example, "05 September, 2022".
If you wanted, you could also include other options, such as the 'yearRange' to only show 3 years at a time, or the 'showClearBtn' as 'true'.
For demonstration purposes, we include the 'i18n' option, which itself will contain a dictionary of elements.
The 'i18n' is the nickname given for 'internationalization' since there are 18 letters in the middle of that word, starting with I and ending with N.
It allows programmers to customize text when dealing with foreign languages, if you want the datepicker element to be translated into Gaelic or Klingon for example.
In this case, I'd like to change the text on the 'Done' button, instead of showing 'OK', I want it to show 'Select'.
Using the list provided, you can change any of these, such as the months, dates, days of the week, etc.
*/
    // select initialization
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);
    // call this variable 'selects' for any select element found, and then initialize those below

    // collapsible initializataion
    let collapsibles = document.querySelectorAll(".collapsible");
    M.Collapsible.init(collapsibles);

});

// Remember, since we've added custom JavaScript, you might need to hard-reload the page in
// order for the static files on our browser to be updated.