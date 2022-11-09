# We want to provide an account reference from the customer account number
# and sort code. However due to issues in the test data, these values are not 
# populated. So we have a mapping here
ACCOUNT_MAPPING = {
    ('72001236', '516112'): {
        "reference": "1d02ae79-b0a5-456f-bb98-96969e2e655c",
    },
    ('87512346', '116413'): {
        "reference": "22f9520c-aa02-4a28-be40-aed7b2205251",
    },
    ('12354987', '784422'): {
        "reference": "38ae7b40-fb9a-42e3-9b81-9285de7f76de",
    },
    ('94675312', '197896'): {
        "reference": "5970839e-61f2-4d3a-becc-5f49e6690a38",
    },
    ('13467985', '558899'): {
        "reference": "6c96b9ab-7751-48e6-9213-9a9bbd8dd2c9",
    },
    ('97546123', '516145'): {
        "reference": "6ce332c0-ba65-4afb-8d65-9107a55d4db9",
    },
    ('19734682', '615144'): {
        "reference": "793e93c2-1c8f-438a-8f05-ea36587057ec",
    },
    ('36523698', '451112'): {
        "reference": "a9b362a7-ba80-4ca2-83e8-e5d28d4388a5",
    },
    ('87452154', '954511'): {
        "reference": "b3ea8d6d-206b-4f60-8e7e-085a6f52395c",
    },
    ('97525241', '721609'): {
        "reference": "dae607fa-d32a-4d83-9613-babe1f8db99a",
    },
    ('94563287', '012331'): {
        "reference": "f83160f4-6284-4179-b841-81f43126f45a",
    },    
}