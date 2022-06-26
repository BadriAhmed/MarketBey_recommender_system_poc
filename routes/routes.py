from fastapi import APIRouter, HTTPException, UploadFile, File
from loguru import logger

from service.recommender import prepare_dataframe_from_json, create_text_column_and_indices, create_similarity_matrix, \
    get_recommendations, response_envelop

route = APIRouter()

df = prepare_dataframe_from_json()
df, indices = create_text_column_and_indices(df)
cosine_sim = create_similarity_matrix(df)


@route.get("/recommendation")
def get_product_recommendation(product_id: str):
    try:
        recommendations = get_recommendations(product_id=product_id,
                                              indices=indices,
                                              dataframe=df,
                                              cosine_sim=cosine_sim)
        return response_envelop(recommendations)
    except KeyError as error:
        logger.error(
            "Product not found", error)
        raise HTTPException(status_code=404, detail="Requested product ID not found")


@route.post("/update_products")
async def update_product_list(uploaded_file: UploadFile = File(...)):
    global df
    global indices
    global cosine_sim
    file_location = "products.json"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    logger.info("Updating recommender system")
    df = prepare_dataframe_from_json()
    df, indices = create_text_column_and_indices(df)
    cosine_sim = create_similarity_matrix(df)
    return "success"
