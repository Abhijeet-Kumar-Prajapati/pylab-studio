# # def http_ status):
# #      match status:
# #      cased 200: rturn "ok" case 404: return "not found" case 500:
# #      return "internal server error" case_: return "unknown satus"



# def http_status(status):
#     match status:
#         case 200:
#             return "ok"
#         case 404:
#             return "not found"
#         case 500:
#             return "internal server error"
#         case _:
#             return "unknown status"
# print(htto_status(500))






def http_status(status):
    match status:
        case 200:
            return "ok"
        case 404:
            return "not found"
        case 500:
            return "internal server error"
        case _:
            return "unknown status"

print(http_status(500))
