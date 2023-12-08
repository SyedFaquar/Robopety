# import bcrypt
# import json
# from google.cloud import storage
# from datetime import datetime, timedelta

# password = "admin"
# bytes = password.encode('utf-8')
# salt = bcrypt.gensalt()
# hash = bcrypt.hashpw(bytes, salt)

# attemp_pw = "admin"
# print(bcrypt.checkpw(attemp_pw.encode('utf-8'), hash))


# data = [{"id":1,"name":"azumarill","photo_url":"https://storage.cloud.google.com/robo_images/azumarill.png"},{"id":2,"name":"alcremie","photo_url":"https://storage.cloud.google.com/robo_images/alcremie.png"},{"id":3,"name":"armarouge","photo_url":"https://storage.cloud.google.com/robo_images/armarouge.png"},{"id":4,"name":"blaziken","photo_url":"https://storage.cloud.google.com/robo_images/blaziken.png"},{"id":5,"name":"blipbug","photo_url":"https://storage.cloud.google.com/robo_images/blipbug.png"},{"id":6,"name":"bramblin","photo_url":"https://storage.cloud.google.com/robo_images/bramblin.png"},{"id":7,"name":"breloom","photo_url":"https://storage.cloud.google.com/robo_images/breloom.png"},{"id":8,"name":"camerupt","photo_url":"https://storage.cloud.google.com/robo_images/camerupt.png"},{"id":9,"name":"charmander","photo_url":"https://storage.cloud.google.com/robo_images/charmander.png"},{"id":10,"name":"cottonee","photo_url":"https://storage.cloud.google.com/robo_images/cottonee.png"},{"id":11,"name":"croconaw","photo_url":"https://storage.cloud.google.com/robo_images/croconaw.png"},{"id":12,"name":"donphan","photo_url":"https://storage.cloud.google.com/robo_images/donphan.png"},{"id":13,"name":"dragalge","photo_url":"https://storage.cloud.google.com/robo_images/dragalge.png"},{"id":14,"name":"dwebble","photo_url":"https://storage.cloud.google.com/robo_images/dwebble.png"},{"id":15,"name":"escavalier","photo_url":"https://storage.cloud.google.com/robo_images/escavalier.png"},{"id":16,"name":"finizen","photo_url":"https://storage.cloud.google.com/robo_images/finizen.png"},{"id":17,"name":"gardevoir","photo_url":"https://storage.cloud.google.com/robo_images/gardevoir.png"},{"id":18,"name":"geodude","photo_url":"https://storage.cloud.google.com/robo_images/geodude.png"},{"id":19,"name":"groudon","photo_url":"https://storage.cloud.google.com/robo_images/groudon.png"},{"id":20,"name":"gulpin","photo_url":"https://storage.cloud.google.com/robo_images/gulpin.png"},{"id":21,"name":"hippowdon","photo_url":"https://storage.cloud.google.com/robo_images/hippowdon.png"},{"id":22,"name":"igglybuff","photo_url":"https://storage.cloud.google.com/robo_images/igglybuff.png"},{"id":23,"name":"iron_thorns","photo_url":"https://storage.cloud.google.com/robo_images/iron_thorns.png"},{"id":24,"name":"kilowattrel","photo_url":"https://storage.cloud.google.com/robo_images/kilowattrel.png"},{"id":25,"name":"kricketot","photo_url":"https://storage.cloud.google.com/robo_images/kricketot.png"},{"id":26,"name":"lampent","photo_url":"https://storage.cloud.google.com/robo_images/lampent.png"},{"id":27,"name":"latias","photo_url":"https://storage.cloud.google.com/robo_images/latias.png"},{"id":28,"name":"latios","photo_url":"https://storage.cloud.google.com/robo_images/latios.png"},{"id":29,"name":"leavanny","photo_url":"https://storage.cloud.google.com/robo_images/leavanny.png"},{"id":30,"name":"linoone","photo_url":"https://storage.cloud.google.com/robo_images/linoone.png"},{"id":31,"name":"pichu","photo_url":"https://storage.cloud.google.com/robo_images/pichu.png"},{"id":32,"name":"pignite","photo_url":"https://storage.cloud.google.com/robo_images/pignite.png"},{"id":33,"name":"primarina","photo_url":"https://storage.cloud.google.com/robo_images/primarina.png"},{"id":34,"name":"psyduck","photo_url":"https://storage.cloud.google.com/robo_images/psyduck.png"},{"id":35,"name":"revavroom","photo_url":"https://storage.cloud.google.com/robo_images/revavroom.png"},{"id":36,"name":"rotom","photo_url":"https://storage.cloud.google.com/robo_images/rotom.png"},{"id":37,"name":"salazzle","photo_url":"https://storage.cloud.google.com/robo_images/salazzle.png"},{"id":38,"name":"scream_tail","photo_url":"https://storage.cloud.google.com/robo_images/scream_tail.png"},{"id":39,"name":"seadra","photo_url":"https://storage.cloud.google.com/robo_images/seadra.png"},{"id":40,"name":"sewaddle","photo_url":"https://storage.cloud.google.com/robo_images/sewaddle.png"},{"id":41,"name":"shiinotic","photo_url":"https://storage.cloud.google.com/robo_images/shiinotic.png"},{"id":42,"name":"slaking","photo_url":"https://storage.cloud.google.com/robo_images/slaking.png"},{"id":43,"name":"staravia","photo_url":"https://storage.cloud.google.com/robo_images/staravia.png"},{"id":44,"name":"swanna","photo_url":"https://storage.cloud.google.com/robo_images/swanna.png"},{"id":45,"name":"totodile","photo_url":"https://storage.cloud.google.com/robo_images/totodile.png"},{"id":46,"name":"tynamo","photo_url":"https://storage.cloud.google.com/robo_images/tynamo.png"},{"id":47,"name":"urshifu","photo_url":"https://storage.cloud.google.com/robo_images/urshifu.png"},{"id":48,"name":"vanilluxe","photo_url":"https://storage.cloud.google.com/robo_images/vanilluxe.png"},{"id":49,"name":"vivillon","photo_url":"https://storage.cloud.google.com/robo_images/vivillon.png"},{"id":50,"name":"yveltal","photo_url":"https://storage.cloud.google.com/robo_images/yveltal.png"}]
# response = {'status':'success', 'data':data[0]}
# def generate_signed_url(bucket_name, object_name, expiration_time=3600):
#     client = storage.Client('service-798990298837@gs-project-accounts.iam.gserviceaccount.com')
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(object_name)

#     expiration = datetime.utcnow() + timedelta(seconds=expiration_time)
#     return blob.generate_signed_url(expiration=expiration)

# signed_url = generate_signed_url('robo_images', 'gs://robo_images/alcremie.png')
# print(signed_url)

# =====================================================================================
# import jwt
# jwt_secret = 'secret'

# payload = {
#         'id': 1,
#         'username': 'John',
#         'user_robot': -1,
#         'all_robots': 'test'
#     }
# print(jwt_secret)
# token = jwt.encode(payload=payload,key=jwt_secret)

# decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
# print(decoded_data)

# =========================================================================================
robot_id = 1
user_id = 12
user_response = {'status': 'success', 'data': {'id': 4, 'user_id': 12, 'robot_id': 1, 'action': 'pick'}}
print(user_response['status'] == "success" and user_response['data']['robot_id'] == robot_id and user_response['data']['action'] == 'pick')
robot_response = {'status': 'success', 'data': {'id': 4, 'user_id': 12, 'robot_id': 1, 'action': 'pick'}}
print(robot_response['status'] == "success" and robot_response['data']['user_id'] == user_id and user_response['data']['action'] == 'pick')
print(int('1') == 1)