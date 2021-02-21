let starRate = {
    init: function(){
        let optionsProf = {
            max_value: 5,
            step_size: 1,
            update_input_field_name: $("#star-prof"),
        }

        let optionsPers = {
            max_value: 5,
            step_size: 1,
            update_input_field_name: $("#star-pers"),
        }

        $('.star-prof').rate(optionsProf);
        $('.star-pers').rate(optionsPers);
    }
}

export { starRate }