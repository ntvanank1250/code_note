 ###################################### thêm giá và child shopify
	if convert['children']:
			for child in convert['children']:
				child_id=to_str(self.get_map_field_by_src(self.TYPE_CHILD, child['id'], child['code']))
				self.log(child_id,"child_id")
				var_post_data={
						"variant": {
							'price': child['price'],
					}
				}
				var_response = self.api('variants/' + to_str(child_id) + '.json', var_post_data, 'Put')
				var_response = json_decode(var_response)
		else:
			product_id=to_str(self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code']))
			get_response = self.api('products/' + to_str(product_id) + '.json', api_type='get')
			get_response = json_decode(get_response)
			variant_id=get_response['product']['variants'][0]['id']
			var_post_data={
						"variant": {
							'price': to_str(round(to_decimal(convert['price']), 2)) if to_decimal(convert['price']) > 0 else 0,
					}
				}
			response = self.api('variants/' + to_str(variant_id) + '.json', var_post_data, 'Put')
			response = json_decode(response)	
################################### Create api shopify:
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
#################### Xóa entity trên target và trên map shopify:
    order_id = self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code'])
    self.api('orders/' + to_str(order_id) + '.json', api_type='Delete')
    self.delete_obj(TABLE_MAP, {'migration_id': self._migration_id, 'type': self.TYPE_ORDER, 'id_desc': order_id})
#################### Thêm themes
	product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
	if product_id:
		# upload file and add to metafield
		if "files" in convert and convert['files']:
			theme_id = 132918018298		
			for file in convert['files']:
				file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
				if not file_code:
					asset_put_file_data = {
						"asset": {
							"key": "assets/{}".format(file['handle']),
							"theme_id": theme_id,
							"src": file['url']
						}
					}
					upload_file_res = self.api(f"themes/{theme_id}/assets.json", asset_put_file_data, "PUT")
					self.log(upload_file_res, '__upload_file_res')
					upload_file_data = dict(json_decode(upload_file_res))
					if "asset" in upload_file_data and upload_file_data["asset"]:
						self.log(upload_file_data, '__upload_file_data')
						self.insert_map('pdf', id_src= file['id'], code_src= file['url'], code_desc= upload_file_data["asset"]['public_url'])

			if len(convert['files']) <= 1:
				for file in convert['files']:
					file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
					self.log(file_code,'__file_code')
					if file_code:
						meta_file_post_data = {
							"metafield": {
								"key": "PDF",
								"value": file_code,
								"namespace": "global",
								"owner_id": product_id,
								"type": "url"
							}
						}
						file_res = self.api("products/{}/metafields.json".format(product_id), meta_file_post_data, "POST")
						self.log(file_res,'__file_res')
			elif len(convert['files']) > 1:
				for i, file in enumerate(convert['files']):
					file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
					self.log(file_code,'__file_code')
					if file_code:
						meta_file_post_data = {
							"metafield": {
								"key": f"PDF_{i}",
								"value": file_code,
								"namespace": "global",
								"owner_id": product_id,
								"type": "url"
							}
						}
						file_res = self.api("products/{}/metafields.json".format(product_id), meta_file_post_data, "POST")
						self.log(file_res,'__file_res')
###########################
		# product_get = self.api(f"products/{product_id}.json", api_type= "GET")
		# product_get = json_decode(product_get)
		# new_tags = ''
		# tags_change = {
		# 	"Stationsausbau Stationsausbau": "Stationsausbau",
		# 	"Stationsausbau": "Stationsausbau inkl. Zubehör",
		# 	"Türen": "Türen inkl. Zubehör",
		# 	"Türen Türen": "Türen"
		# }
		# tags = product_get["product"]["tags"].split(",")
		# for one_tag in tags:
		# 	if one_tag in tags_change:
		# 		one_tag = tags_change[one_tag]
		# 	new_tags += one_tag
		# update_product_data = {
		# 	"product": {
		# 		"tags": new_tags
		# 	}
		# }
		# product_response = self.api(f"products/{product_id}.json", data= update_product_data, api_type= "PUT")

		# new_tags = ""
		# for cate in convert["categories"]:
		# 	category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, cate['id'], cate['code'])
		# 	category_get = self.api(f"collections/{category_id}.json", api_type= "GET")
		# 	category_get = json_decode(category_get)
		# 	new_tags = new_tags + category_get["collection"]["title"] + ","
		# if new_tags[-1] == ",":
		# 	new_tags = new_tags[:-1]
		# update_product_data = {
		# 	"product": {
		# 		"tags": new_tags
		# 	}
		# }
		# product_response = self.api(f"products/{product_id}.json", data= update_product_data, api_type= "PUT")

