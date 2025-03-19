from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# @app.get('/')
# async def root():
#     return {"message" : "Hello Hynger Birds!!"}
ongoing_order = {}

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)

    

def add_to_order(parameters: dict, session_id):
    food_items = parameters["food-items"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_items = dict(zip(food_items, quantities))
        # if session id already exist in ongoing order
        if session_id in ongoing_order:
            for item, quant in new_food_items.items():
                # if the food item already exist for the session id then increase the quantity
                if item in ongoing_order[session_id]:
                    ongoing_order[session_id][item] += quant
                else:
                    # if the food item does not exist for the session id then update with item and quantity
                    ongoing_order[session_id].update({item: quant})
        else:
            ongoing_order[session_id] = new_food_items
        
        # extract the items placed for order by the customer and ask for anything else req
        ordered_items_so_far = generic_helper.get_str_from_food_dict(ongoing_order[session_id])
        fulfillment_text = f"food items ordered so far = {ordered_items_so_far}.\n Do you need anything else??"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id):
    # if no session_id found
    if session_id not in ongoing_order:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })
    
    food_items = parameters["food-items"]
    quantities = parameters["number"]

    current_order = ongoing_order[session_id]
    
    removed_items = []      #list of items removed
    no_such_items = []      #items asked to remove but does not exist in the order list
    
    print(current_order)
    print(food_items)
    i=0
    fulfillment_text = ''
    for item in food_items:
        print(item)
        if item not in current_order:
            no_such_items.append(item)
        else:
            if quantities[i] > current_order[item]:
                fulfillment_text = f'The quantity to remove for {item} is more than what you ordered! specify quantity again.\n'
            else:
                current_order[item] -= quantities[i]
                removed_items.append((item, quantities[i]))
                if current_order[item] == 0:
                    del current_order[item]         # Item removed
        i+=1

    print('removed items = ', removed_items)
    if len(removed_items) > 0:
        fulfillment_text += f'Removed {", ".join([f"{value} {key}" for key, value in removed_items])} from your order!\n'

    if len(no_such_items) > 0:
        fulfillment_text += f'Your current order does not have {",".join(no_such_items)}.\n'

    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty! You can say 'Place a New Order' or 'Track Order'."
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}.\nAnything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })




def complete_order(parameters: dict, session_id):
    # If session id not exist in ongoing order (due to any connection issue), again place order
    if session_id not in ongoing_order:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        # order needs to be added in the database
        # get order list from session id
        order_list = ongoing_order[session_id]

        # get order id after saving the order in db
        if len(order_list)==0:
            fulfillment_text = "Sorry, your order list is empty! We couldn't process your order. " \
                               "Appologies for the inconvenience!! "\
                               "Thank you for Visiting!"
            
        else:
            order_id = save_to_db(order_list)
            if order_id == -1:
                fulfillment_text = "Sorry, MomotoX is super drained and down. We couldn't process your order due to a backend error. " \
                                "Appologies for the inconvenience!! "\
                                "Please place a new order again after some time."
            else:
                # get the total amount for the order
                order_total = db_helper.get_total_order_price(order_id)

                fulfillment_text = f"Awesome. We have placed your order. " \
                            f"Here is your order id # {order_id}. " \
                            f"Your order total is {order_total} which you can pay at the time of delivery!"

        del ongoing_order[session_id]



    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order_list: dict):
    # get order id
    order_id_for_curr = db_helper.get_next_order_id()

    # Inserting individual items along with the quantity in orders table
    for food_item, quantity in order_list.items():

        # add the items to db
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            order_id_for_curr
        )

        # if rcode = -1 (error insterting items)
        if rcode == -1:
            return -1
        
    # Now insert order tracking status in the tracking table with order_id
    db_helper.insert_order_tracking(order_id_for_curr, "in progress")
        
    return order_id_for_curr

   


def track_order(parameters: dict, session_id):
    # print(parameters)
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

        