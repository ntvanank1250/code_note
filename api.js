function create_api(ver = 'new') {
    if (ver == 'new') {
        var checkBoxs = document.querySelectorAll('.Polaris-Checkbox__Input_30ock');
        var index = 0;
        checkBoxs.forEach(check => {
            if (check.checked != true) {
                check.click();
                setTimeout(() => { console.log("Enable checkbox " + index) }, 1000);
                index += 1;
            } else {
                return;
            }
        });
    } else {
        document.getElementById('api_client_title').value = 'litextension';
        document.getElementById('api_client_contact_email').value = 'contact@litextension.com';

        const function_list = document.querySelectorAll("[name='api_client[access_scope][]']");
        for (let index = 0; index < function_list.length; index++) {
            let attr_id = function_list[index].getAttribute('id');
            if (attr_id.indexOf('[') == -1) {
                continue
            }
            options = function_list[index].getElementsByTagName('option');
            if (options.length == 0) {
                continue
            }
            options[options.length - 1].selected = 'selected';
        }
    }
}
create_api();