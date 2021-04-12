import psutil
from flask import Blueprint
from hurry.filesize import size

from app.authentication import authenticate
from app.config import ROOT_PATH

bp = Blueprint('disk_usage', __name__)


@bp.route('/disk_usage/', methods=['GET'])
@authenticate
def get_disk_info(token_dir):
    disk_info = psutil.disk_usage(ROOT_PATH)
    return {'free': size(disk_info.free),
            'used': size(disk_info.used),
            'total': size(disk_info.total)}, 200
