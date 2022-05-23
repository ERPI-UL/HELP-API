
from fastapi import APIRouter, Depends, HTTPException, status, Body
import utils
import Models

router = APIRouter()


@router.post('/changeAdminLevel/{idUser}')
async def changeAdminLevel(idUser: int, adminLevel: int = Body(..., embed=True),  bool: bool = Depends(utils.AdminRequired), current_user: Models.User = Depends(utils.get_current_user_in_token)):
    user = await Models.User.get(id=idUser)
    if user.adminLevel == current_user.adminLevel:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Vous ne pouvez pas changer le role d'un utilisateur de votre niveau")
    if adminLevel >= utils.Permission.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez pas mettre un niveau d'administration plus élevé que le votre"
        )
    user.adminLevel = adminLevel
    await user.save()
    return await Models.UserinFront.from_tortoise_orm(user)


@router.delete('/deleteUser/{idUser}')
async def deleteUser(idUser: int, bool: bool = Depends(utils.AdminRequired), current_user: Models.User = Depends(utils.get_current_user_in_token)):
    user = await Models.User.get(id=idUser)
    if user.adminLevel == current_user.adminLevel:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Vous ne pouvez pas supprimer un administrateur")
    await user.delete()
    return {'message': 'Utilisateur supprimé'}


@router.get('/logs')
async def logs(current_user: Models.User = Depends(utils.AdminRequired)):
    try:
        file = open('logs.txt', 'r')
        log = []
        while True:
            line = file.readline()
            if not line:
                break
            if line != '\n':
                log.append(line)
        return log
    except IOError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le fichier n'existe pas"
        )
