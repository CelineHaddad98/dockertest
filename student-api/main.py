from fastapi import FastAPI
from uuid import UUID

from db import engine, address
from fastapi import FastAPI, HTTPException, status
from classes import AddressPatch, AddressPost, AddressPut, AddressResponse
from session_handle import JSONResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()


@app.get('/address/{id}')
def get_address_by_id(id:UUID) -> JSONResponse:
    with engine.connect() as conn:
        address_info= conn.execute(address.select().where(
            address.c.id == id)).first()
    if not address_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Address with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': AddressResponse(**address_info._asdict())}
    )



@app.get('/address')
def get_all_address() -> JSONResponse:
    with engine.connect() as conn:
        address_info= conn.execute(address.select()).fetchall()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': (AddressResponse(**addresses._asdict())
         for addresses in address_info)}
    )


@app.post('/address',response_model=AddressResponse)
def add_address(addresses: AddressPost) -> JSONResponse:
    try:
        with engine.begin() as conn:
            new_address = conn.execute(address.insert().returning(
                address).values(**addresses.dict()))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad data')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': new_address.first()}
    )



@app.delete('/address/{id}')
def delete_address(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        address_deleted = conn.execute(
            address.delete().where(address.c.id == id)).rowcount

    if not address_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': f"address with id {id} has been deleted"}
    )






@app.patch("/address/{id}", response_model=AddressResponse)
def update_student(addresse: AddressPatch, address_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        updated_address = conn.execute(address.update().where(
            address.c.id == address_id)
            .values(**addresse.dict(exclude_none=True)).returning(address))

        if not updated_address.rowcount:
            raise HTTPException(
                status_code=404,
                detail=f'Address with id: ({address_id}) dose not exist'
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': updated_address.first()}
        )




@app.put("/address/{id}", response_model=AddressResponse)
def put_address(new_address: AddressPut, address_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        deleted_address = conn.execute(address.delete().where(
            address.c.id == address_id
        )).rowcount

        added = conn.execute(
            address.insert().values(id=address_id,
                                     ** new_address.dict()).returning(address))

        if not deleted_address:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {address_id} dose not exist')

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={
                            'data': AddressResponse(**added.first())
                        })