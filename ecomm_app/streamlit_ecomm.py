import streamlit as st
from PIL import Image
import logging
import boto3
import json
from botocore.exceptions import EndpointConnectionError, ClientError

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure AWS credentials 
kinesis_client = boto3.client('kinesis', region_name='ap-south-1')
dynamodb_client = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb_client.Table('ProductDataTable')

stream_name = 'ecommdatastream'

# Dummy data for product details
PRODUCT_DETAILS = {
    'ECOMM100001': {
        'pic': 'images/iphone.png',
        'title': 'Apple iPhone 15 Pro Max',
        'description': '256 GB / Natural Titanium',
        'price': '₹1,49,900/-'
    },
    'ECOMM100002': {
        'pic': 'images/nike.png',
        'title': 'Nike Air Zoom Pegasus 37',
        'description': 'Comfortable running shoes',
        'price': '₹9,999/-'
    },
    'ECOMM100003': {
        'pic': 'images/tshirt.png',
        'title': 'Louis Vuitton T-Shirt',
        'description': 'Cotton Printed Superior Tshirt for Men & Women',
        'price': '₹25,000/-'
    },
    'ECOMM100004': {
        'pic': 'images/bag.png',
        'title': 'Wildcraft Laptop Backpack',
        'description': 'Durable and spacious bag - 15 inch with 2 compartments',
        'price': '₹2,149/-'
    }
}

def home_page():
    st.title('Welcome to my Ecommerce platform!')
    st.write('What do you want to buy today?')

    # Initialize click counts if not present
    if 'click_counts' not in st.session_state:
        st.session_state['click_counts'] = {
            'ECOMM100001': 0,
            'ECOMM100002': 0,
            'ECOMM100003': 0,
            'ECOMM100004': 0
        }

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        img_phone = Image.open('images/iphone.png')
        st.image(img_phone, caption='Apple iPhone 15 Pro Max', use_column_width='auto')
        if st.button('View Details', key='button1'):
            st.session_state['selected_product'] = 'ECOMM100001'
            st.session_state['page'] = 'product'
            logger.info('Navigated to product details page for iPhone..')
            st.session_state['click_counts']['ECOMM100001'] += 1
            send_to_kinesis('ECOMM100001', 'Apple iPhone 15 Pro Max', st.session_state['click_counts']['ECOMM100001'])
            logger.info('Click count of iPhone sent to kinesis..')

    with col2:
        img_shoes = Image.open('images/nike.png')
        st.image(img_shoes, caption='Nike Air Zoom Pegasus 37', use_column_width='auto')
        if st.button('View Details', key='button2'):
            st.session_state['selected_product'] = 'ECOMM100002'
            st.session_state['page'] = 'product'
            logger.info('Navigated to product details page for Nike shoes..')
            st.session_state['click_counts']['ECOMM100002'] += 1
            send_to_kinesis('ECOMM100002', 'Nike Air Zoom Pegasus 37', st.session_state['click_counts']['ECOMM100002'])
            logger.info('Click count of Nike shoes sent to kinesis..')

    with col3:
        img_lap = Image.open('images/tshirt.png')
        st.image(img_lap, caption='Louis Vuitton T-Shirt', use_column_width='auto')
        if st.button('View Details', key='button3'):
            st.session_state['selected_product'] = 'ECOMM100003'
            st.session_state['page'] = 'product'
            logger.info('Navigated to product details page for LV t-shirt..')
            st.session_state['click_counts']['ECOMM100003'] += 1
            send_to_kinesis('ECOMM100003', 'Louis Vuitton T-Shirt', st.session_state['click_counts']['ECOMM100003'])
            logger.info('Click count of LV t-shirt sent to kinesis..')

    with col4:
        img_bag = Image.open('images/bag.png')
        st.image(img_bag, caption='Wildcraft Laptop Backpack', use_column_width='auto')
        if st.button('View Details', key='button4'):
            st.session_state['selected_product'] = 'ECOMM100004'
            st.session_state['page'] = 'product'
            logger.info('Navigated to product details page for backpack..')
            st.session_state['click_counts']['ECOMM100004'] += 1
            send_to_kinesis('ECOMM100004', 'Wildcraft Laptop Backpack', st.session_state['click_counts']['ECOMM100004'])
            logger.info('Click count of backpack sent to kinesis..')

    if st.button('Most Viewed Products'):
        most_viewed_product()

def product_page():
    product_id = st.session_state.get('selected_product', None)
    if product_id and product_id in PRODUCT_DETAILS:
        product = PRODUCT_DETAILS[product_id]

        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(product['pic'])
            st.image(img, use_column_width='auto')
        with col2:
            st.write(f"Product ID: {product_id}")
            st.write(product['title'])
            st.write(product['description'])
            st.write(product['price'])

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                st.button('Buy Now!', key='buy_now')
            with btn_col2:
                st.button('Add to cart', key='add_cart')
            with btn_col3:
                st.button('Add to favourites', key='add_fav')

    if st.button('Go Back'):
        st.session_state['page'] = 'home'
        logger.info('Navigated back to home page')

def send_to_kinesis(product_id, product_name, click_count):
    data = json.dumps({
        'product_id': product_id,
        'product_name': product_name,
        'click_count': click_count
    })

    try:
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=data,
            PartitionKey=product_id
        )
        logger.info('Data sent to Kinesis: %s', data)
    except EndpointConnectionError as e:
        logger.error('Failed to send data to Kinesis: %s', e)
    except ClientError as e:
        logger.error('AWS ClientError: %s', e)

def most_viewed_product():
    try:
        response = table.scan()
        items = response['Items']
        if items:
            most_viewed = max(items, key=lambda x: x['click_count'])
            st.session_state['selected_product'] = most_viewed['product_id']
            st.session_state['page'] = 'product'
            logger.info('Navigated to product details page for most viewed product')
        else:
            st.write("No product views found.")
    except ClientError as e:
        logger.error('Error fetching most viewed product: %s', e)
        st.write("Error fetching most viewed product.")

# Initialize the session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
    logger.info('Session state initialized to home')

# Display appropriate page based on session state
if st.session_state['page'] == 'home':
    home_page()
elif st.session_state['page'] == 'product':
    product_page()
