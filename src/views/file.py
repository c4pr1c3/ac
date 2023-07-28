from flask import Blueprint, render_template, flash, redirect, request
from hmac_1 import hamc_encrypt, random_within_7_days, within_7_days
from models import File
from common import *
from flask import current_app as app
from datetime import date, datetime, timedelta


file = Blueprint('file', __name__)


@file.route('/')
@login_required
def get__file(user):
    from models import File
    app.logger.debug("get__file with user.id_=%s", user)
    files = File.query.filter(File.creator_id == user.id_).all()
    return render_template('file.html', username=user.username, files=files)


@file.route('/upload')
@login_required
def get__upload():
    from form import FileForm
    return render_template('file_upload.html', form=FileForm())


@file.route('/upload', methods=['POST'])
@login_required
def post__upload(user):
    try:
        from form import FileForm
        form = FileForm()
        assert form.validate_on_submit(), 'invalid form fields'
        data = form.file.data
        File.upload_file(user, data)
        flash('上传成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('上传失败！'+message)
    return redirect('/file')


@file.route('/remove')
@login_required
def get__remove(user):
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        File.delete_file(user, filename)
        flash('删除成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('删除失败！'+message)
    return redirect('/file')


@file.route('/download')
@login_required
def get__download(user):
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        # key = random_within_7_days()
        # hamc_encrypt(filename, key)
        # assert hamc_encrypt, 'Exceeded download time' 
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'plaintext', 'signature', 'hashvalue'), 'unknown type'
        return File.download_file(user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！'+message)
        return redirect('/file')


@file.route('/share')
@login_required
def get__share(user):
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        File.share_file(user, filename)
        flash('设置成功！')
        return redirect('/file')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('设置失败！'+message)
        return redirect('/file')
    
# @file.route('/url', summary="上传url预签名")
# @login_required
# def presigned_url(query: ObjectQuery):
#     url = minio_client.presigned_put_object(query.bucket_name, query.object_name, expires=timedelta(days=1))
#     print(url)
#     return response(data=url)
