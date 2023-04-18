
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.models import User, UserinFront
import app.utils
from app.utils import admin_required, Permission, get_current_user_in_token
router = APIRouter()


@router.post('/changeAdminLevel/{id_user}')
async def change_admin_level(id_user: int, admin_level: int = Body(..., embed=True),  _=Depends(admin_required),
                             current_user: User = Depends(get_current_user_in_token)):
    """ Change the admin level of a user if you are an admin"""
    user = await User.get(id=id_user)
    if user.adminLevel == current_user.adminLevel:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Vous ne pouvez pas changer le role d'un utilisateur de votre niveau")
    if admin_level >= app.utils.Permission.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez pas mettre un niveau d'administration plus élevé que le votre"
        )
    user.adminLevel = admin_level
    await user.save()
    return await UserinFront.from_tortoise_orm(user)


@router.delete('/deleteUser/{id_user}')
async def delete_user(id_user: int, _=Depends(admin_required)):
    """ Delete a user if you are an admin"""
    user = await User.get(id=id_user)
    if user.adminLevel == Permission.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Vous ne pouvez pas supprimer un administrateur")
    await user.delete()
    return {'message': 'Utilisateur supprimé'}
