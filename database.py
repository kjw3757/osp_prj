import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        

    def insert_item(self, name, data, img_paths, seller_id):
        item_info = {
            "name": name,  # 이 부분을 추가하여 상품 이름을 지정
            "seller": seller_id, #현재 로그인한 사용자의 id로 설정
            "addr": data['addr'],
            "category": data['category'],
            "card": data['card'],
            "status": data['status'],
            "phone": data['phone'],
            "price": data['price'],
            "description": data['description'],
            "img_paths": img_paths
        }
        self.db.child("item").child(name).set(item_info)
        return True

    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'], "pw": pw, "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if str(users.val()) == "None":  # first registration
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
                    return False
                return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()

            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

    def search_items(self, search_keyword):
        items = self.db.child("item").get()
        results = []

        for res in items.each():
            value = res.val()

            if "name" in value and search_keyword in value["name"]:
                results.append(value)


        return results  # 이 부분을 추가하여 검색 결과를 반환합니다.

    def delete_item(self, name):
        try:
            # 아이템 삭제
            self.db.child("item").child(name).remove()
            return True
        except Exception as e:
            return False

    def reg_review(self, data, img_path, user_id, seller_id):
        review_info ={
            "title": data['title'],
            "rate": data['reviewStar'],
            "review": data['reviewContents'],
            "reviewer": user_id,
            "seller_id": seller_id,
            "img_path": img_path
        }
        self.db.child("review").child(data['name']).set(review_info)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_review_byname(self, name):
        review_data = self.db.child("review").child(name).get().val()
        return review_data

    def get_user_reviews(self, user_id):
        user_reviews = []
        reviews = self.db.child("review").get().val()

        if reviews is not None:
            for review_name, review_data in reviews.items():
                if 'reviewer' in review_data and review_data['reviewer'] == user_id:
                    user_reviews.append({"name": review_name, "data": review_data})
        return user_reviews


    def get_likes(self, user_id):
        likes = self.db.child("heart").child(user_id).get()
        likes_list = []

        if likes.val() is not None:
            for item in likes.each():
                if item.val()['interested'] == 'Y':
                    # 상품 이름과 함께 이미지 경로와 가격도 가져옵니다.
                    item_name = item.key()
                    item_data = self.db.child("item").child(item_name).get().val()
                    if item_data is not None:
                        item_img_path = item_data.get("img_paths", "")  # 이미지 경로 필드를 가져옴
                        first_img_path = item_img_path[0]  # 첫 번째 이미지의 경로만 가져오기

                        item_price = item_data.get("price", "")  # 가격 필드를 가져옴
                        likes_list.append({"name": item_name, "img_path": first_img_path, "price": item_price})

        return likes_list


    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
                return target_value

    def update_heart(self, user_id, isHeart, item):
        heart_info ={
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True

    def get_items_bycategory(self, cate):
        items = self.db.child("item").get()
        target_value = []
        target_key = []
        
        for res in items.each():
            value = res.val()
            key_value = res.key()
            
            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
            
        new_dict = {}
        
        for k, v in zip(target_key, target_value):
            new_dict[k] = v
            
        return new_dict

    def get_user_items(self, user_id):
        user_items = []
        items = self.db.child("item").get().val()

        if items is not None:
            for item_name, item_data in items.items():
                if 'seller' in item_data and item_data['seller'] == user_id:
                    user_items.append({"name": item_name, "data": item_data})

        return user_items

    def get_user_items_count(self, user_id):
        # 사용자가 등록한 상품 수를 가져오는 로직을 구현
        user_items_count = 0  # 초기값

        # Firebase Realtime Database에서 사용자가 등록한 상품을 가져옵니다.
        user_items = self.get_user_items(user_id)

        # 사용자가 등록한 상품 수를 개수로 계산
        user_items_count = len(user_items)

        return user_items_count

    def get_user_reviews_count(self, user_id):
        # 사용자가 등록한 상품 수를 가져오는 로직을 구현
        user_reviews_count = 0  # 초기값

        # Firebase Realtime Database에서 사용자가 등록한 상품을 가져옵니다.
        user_reviews = self.get_user_reviews(user_id)

        # 사용자가 등록한 상품 수를 개수로 계산
        user_reviews_count = len(user_reviews)

        return user_reviews_count
