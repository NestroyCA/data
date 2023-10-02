import requests
import glob
from config import br_client, BASEROW_DB_ID, JSON_FOLDER
from acdh_tei_pyutils.tei import TeiReader
import json

editions_path="./xmls/"
places_xpath=".//tei:rs[@type='place']/@target"
places_prefix = "place:"
places_table_id = "2563"
place_id_field = "field_23582"
total_occurences_field = "field_23759"
baserow_nestroy_id_key = "nestroy_id"
baserow_counter_key = "total_occurences"



def count_place_occurences():
    place_id_2_occ_counter = {}
    for file in glob.glob(editions_path):
        doc = TeiReader(file)
        for place_ref in doc.any_xpath(places_xpath):
            place_id = place_ref.removeprefix(places_prefix)
            if place_id not in place_id_2_occ_counter:
                place_id_2_occ_counter[place_id] = 0
            place_id_2_occ_counter[place_id] += 1
    return place_id_2_occ_counter


def update_item_online(item_id:str, update_data:dict):
    update_target_url = f"{br_client.br_base_url}database/rows/table/{places_table_id}/{item_id}/?user_field_names=true"
    result = requests.patch(
        update_target_url,
        headers = {
            "Authorization" : f"Token {br_client.br_token}",
            "Content-Type" : "application/json",
        },
        #json = json.dumps(update_data)
        json=update_data
    )
    return result

def request_place_ids_2_places_from_baserow():
    return dict(
        (place[baserow_nestroy_id_key], place) for place in  br_client.yield_rows(places_table_id)
    )


if __name__ == "__main__":
    place_ids_2_places = request_place_ids_2_places_from_baserow()
    place_ids_2_count = count_place_occurences()
    for quantified_place_id, item in place_ids_2_places.items():
        old_count = item[baserow_counter_key]
        count = place_ids_2_count[quantified_place_id] if quantified_place_id in place_ids_2_count else 0
        if old_count != count:
            update_data = {
                baserow_counter_key : count
            }
            item_id = item['id']
            result = update_item_online(
                item_id,
                update_data
            )
            print(f"update '{item_id}': {result}")