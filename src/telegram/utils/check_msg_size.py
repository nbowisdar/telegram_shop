def divide_big_msg(msg: str) -> list[str]:
    if len(msg) < 4000:
        return [msg]

    return msg.split("\n\n")
    # smaller_msgs = []
    # curr_msg = ""
    # for word in msg.split():
    #     if len(curr_msg + " " + word) > 100:
    #         # Append current msg to list and start a new one
    #         smaller_msgs.append(curr_msg)
    #         curr_msg = ""
    #     curr_msg += " " + word
    # smaller_msgs.append(curr_msg)
    # ret



        # count = 0
    # # before = 0
    # for char in msg:
    #     if count >= 3000 and char == "\n":
    #         resp.append(msg[0:count])
    #         msg = msg[count:]
    #         count = 0
    return resp
