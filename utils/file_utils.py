import codecs
import io


def file_add_bom(filename):
    """
    给一个UTF-8编码的文件增加BOM头，UTF-8-BOM编码。覆盖源文件。
    :param filename:
    :return:
    """
    with open(filename, 'rb') as fr:
        old = fr.read()
    new_io = io.BytesIO()
    new_io.write(codecs.BOM_UTF8)
    new_io.write(old)
    with open(filename, 'wb') as fw:
        fw.write(new_io.getvalue())
