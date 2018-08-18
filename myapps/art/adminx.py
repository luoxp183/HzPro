import xadmin
from xadmin import views

from art.models import Tag, Art


class BaseSetting(object):
    # 主题修改
    enable_themes = False  # 系统资源加载很慢
    use_bootswatch = True


class GlobalSettings(object):
    # 整体配置
    site_title = '美文后台管理系统'
    site_footer = '千锋教育python项目'
    menu_style = 'accordion'  # 菜单折叠

    # 搜索模型
    global_search_models = [Tag, Art]

    # 模型的图标(参考bootstrap图标插件)
    global_models_icon = {
        Art: "glyphicon glyphicon-headphones",
        Tag: "glyphicon glyphicon-play-circle"
    }  # 设置models的全局图标

    # 设置app模块的标题
    apps_label_title = {
        'art': '文章管理'
    }

    # 设置app模块的图标
    apps_icons = {
        'art': 'glyphicon glyphicon-book'
    }


class TagAdmin:
    list_display = ['name', 'add_time']
    search_fields = ['name']


class ArtAdmin:
    list_display = ['title', 'author', 'summary', 'publish_date']
    search_fields = ['title', 'author']
    style_fields = {
        'content': 'ueditor',  # 设置content字段的样式
    }


xadmin.site.register(views.BaseAdminView, BaseSetting)  # 基本后台设置
xadmin.site.register(views.CommAdminView, GlobalSettings)  # 通用设置

xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Art, ArtAdmin)