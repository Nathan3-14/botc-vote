const filter_options = (filter_value) => {
    var options = document.getElementsByName("script");
    var filter_value = filter_value.toLowerCase().replace(" ", "_");
    for (const option of options) {
        var option_value = option.children[0].value.toLowerCase();
        if (option_value.includes(filter_value)) {
            option.style.display = "block";
        } else {
            option.style.display = "none";
        }
    }
}