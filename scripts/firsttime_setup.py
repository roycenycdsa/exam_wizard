
import sys
sys.path.append('.')

from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb

gb.create_grade_book('Test Grade Book', in_domain = True)

print('All done')