import requests, time

url = "https://api.groupme.com/v3"
token = "INSERT TOKEN HERE"

def get_me():
	r = requests.get(url + "/users/me" + "?token=" + token)
	print r.status_code
	me = r.json()["response"]
	print me
	return me

def get_groups():
	r = requests.get(url + "/groups" + "?token=" + token)
	print r.status_code

	
def get_group_id(group_name):
	r = requests.get(url + "/groups" + "?token=" + token)
	print r.status_code
	groups = r.json()["response"]
	for group in groups:
		if(group["name"] == group_name):
			print group["group_id"]
			return group["group_id"]

def create_group(name, description, image_url):
	r = requests.post(url + "/groups" + "?token=" + token, json={"name": name, "description": description, "image_url": image_url}) 
	print r.status_code
	json =  r.json()
	print "Created group " + name
	return json["response"]["group_id"]
	
def rejoin_group(group_id):
	r = requests.post(url + "/groups/join" + "?token=" + token, json={"group_id": group_id})
	print "Rejoining group " + group_id
	print r.status_code

	
def add_members_to_group(group_id, members):
	r = requests.post(url + "/groups/" + group_id + "/members/add" + "?token=" + token, json={"members": members})
	print r.status_code
	print r.json()

def remove_member_from_group(group_id, membership_id):
	r = requests.post(url + "/groups/" + group_id + "/members/" + membership_id + "/remove" + "?token=" + token)
	print r.status_code
	print "Removing " + membership_id + " from group " + group_id
	
def update_nickname(group_id, nickname):
	r = requests.post(url + "/groups/" + group_id + "/memberships/update" + "?token=" + token, json={"membership":{"nickname": nickname}})
	print r.status_code
	
def update_profile(name, image_url):
	r = requests.post(url + "/users/update" + "?token=" + token, json={"name": name, "avatar_url": image_url})
	print "Updating profile"
	print r.status_code
	print r.json()

def reset_profile():
	update_profile("_", None)

def destroy_group(group_id):
	my_id = get_me()["id"]
	print "My id: " + my_id 
	
	r = requests.get(url + "/groups/" + group_id + "?token=" + token)
	print r.status_code
	json = r.json()
	creator_user_id = json["response"]["creator_user_id"]
	print "Creator id: " + creator_user_id
	members = json["response"]["members"]
	group_name = json["response"]["name"]
	group_description = json["response"]["description"]
	group_image_url = json["response"]["image_url"]
	
	
	members_to_add = []
	
	for member in members:
		if member["user_id"] != my_id: 
			
				
			
			if member["user_id"] != creator_user_id:
				members_to_add.append({"nickname": member["nickname"], "user_id": member["user_id"]})
				remove_member_from_group(group_id, member["id"])
			else:
				creator_nickname = member["nickname"]
				creator_image_url = member["image_url"]
				update_profile(creator_nickname, creator_image_url)
		else:
			my_membership_id = member["id"]
	
	print "Waiting a bit"
	time.sleep(3)
	new_group_id = create_group(group_name, group_description, group_image_url)
	print members_to_add
	add_members_to_group(new_group_id, members_to_add)
	remove_member_from_group(group_id, my_membership_id)
	
def leave_group(group_id):
	my_id = get_me()["id"]
	print "My id: " + my_id 
	r = requests.get(url + "/groups/" + group_id + "?token=" + token)
	print r.status_code
	json = r.json()
	members = json["response"]["members"]
	for member in members:
		print "Member user id: " + member["user_id"]
		if(member["user_id"] == my_id):
			my_membership_id = member["id"]
			print "My membership_id: " + my_membership_id
			break
	remove_member_from_group(group_id, my_membership_id)

def leave_group_by_name(group_name):
	group_id = get_group_id(group_name)
	leave_group(group_id)
	
	
def rejoin_group(group_id):
	r = requests.post(url + "/groups/join" + "?token=" + token, json={"group_id": group_id})
	

if __name__ == "__main__":
	group_id = ""
	rejoin_group(group_id)
	destroy_group(group_id)
