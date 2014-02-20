#TODO: Django < 1.6 searches TestCases only in this file.
# As of 1.6 we can remove these imports
from .test_models import TestValidators
from .test_views import (TestArticleList, TestCourseList, TestDownloadList,TestGrantList, TestGrantDetail,
                         TestPeopleList, TestPersonalPages, TestThesesList, TestThesisDetail, TestEmptyDatabase)
