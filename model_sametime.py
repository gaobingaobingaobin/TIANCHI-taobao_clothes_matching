#  -*- coding: utf-8 -*-
def get_user_bought_history():
    f = open("dataset/process/user_bought_history.txt")
    users = {}
    items = {}
    # index = 0
    for line in f:
        line.replace("\n","")
        arr = line.split(" ")
        if users.has_key(arr[0]):
            users[arr[0]].append({"item_id":arr[1],"quarter":arr[2].replace("\n","")})
        else:
            users[arr[0]] = [{"item_id":arr[1],"quarter":arr[2].replace("\n","")}]
        if items.has_key(arr[1]):
            items[arr[1]].append({"user_id":arr[0],"quarter":arr[2].replace("\n","")})
        else:
            items[arr[1]] = [{"user_id":arr[0],"quarter":arr[2].replace("\n","")}]
        # print index
        # index += 1
    return users,items
def get_sametime_items(item,users,items):

    userlist = []
    result = {}
    if items.has_key(item):
        userlist = items[item]
        # print userlist
    for user in userlist:
        itemlist = []
        if users.has_key(user['user_id']):
            quarter = user['quarter']
            itemlist = users[user['user_id']]
            for i in itemlist:
                if i["item_id"] != item:
                    if i['quarter'] == quarter:
                        if result.has_key(i["item_id"]):
                            result[i["item_id"]] = result[i["item_id"]] + 1
                        else:
                            result[i["item_id"]] = 1
    return sorted(result.items(), key=lambda x:x[1],reverse=True)
if __name__ == "__main__":
    users,items = get_user_bought_history()
    f = open("dataset/process/user_bought_history.txt")
    for line in f:
        item = line.replace("\n","")
        result = get_sametime_items(item, users, items)
        arr = []
        for i in result:
            arr.append(i[0])
        print item + " " + str(arr)
