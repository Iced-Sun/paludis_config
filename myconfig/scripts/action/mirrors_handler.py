from action.action_handler import Action_handler

class Mirrors_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?mirrors(.bash)?$'

    #preferred_sites = ['ustc', 'bjtu', 'cqu', 'lzu', 'tsu', 'netease', 'aliyun', 'huawei', 'tencent' ]
    preferred_sites = ['ustc', 'cqu', 'lzu', 'tsu', 'netease', 'aliyun', 'huawei', 'tencent' ]

    ## https://lework.github.io/lemonitor/#/%E6%B5%8B%E9%80%9F
    mirror_sites = {
        'bjtu': {
            'url': 'http://mirror.bjtu.edu.cn',
            'repositories': [
                'apache', 'cpan', 'ctan', 'debian', 'gentoo gentoo/distfiles', 'gnu', 'kernel', 'qt'
            ]
        },
        'cqu': {
            'url': 'http://mirror.cqu.edu.cn',
            'repositories': [
                'cpan CPAN', 'ctan CTAN', 'debian', 'gnu', 'kernel', 'mariadb'
            ]
        },
        'lzu': {
            'url': 'http://mirror.lzu.edu.cn',
            'repositories': [
                'cpan CPAN', 'ctan CTAN', 'debian', 'gentoo gentoo/distfiles', 'gnu'
            ]
        },
        'tsu': {
            'url': 'http://mirrors.tuna.tsinghua.edu.cn',
            'repositories': [
                'apache', 'cpan CPAN', 'ctan CTAN', 'debian', 'flightgear', 'gentoo gentoo/distfiles',
                'gnu', 'libreoffice', 'mysql', 'openbsd', 'postgresql', 'qt', 'videolan videolan-ftp',
                'mariadb'
            ]
        },
        'ustc': {
            'url': 'http://mirrors.ustc.edu.cn',
            'repositories': [
                'apache', 'cpan CPAN', 'ctan CTAN', 'debian', 'gentoo gentoo/distfiles', 'gnome', 'gnu',
                'kde', 'kernel kernel.org', 'postgresql', 'videolan videolan-ftp', 'mariadb'
            ]
        },
        'aliyun': {
            'url': 'https://mirrors.aliyun.com',
            'repositories': [
                'apache', 'cpan CPAN', 'ctan CTAN', 'debian', 'gentoo gentoo/distfiles', 'mariadb'
            ]
        },
        'huawei': {
            'url': 'https://mirrors.huaweicloud.com',
            'repositories': [
                'apache', 'ctan CTAN', 'debian', 'gnu', 'mysql', 'ruby ruby/ruby', 'mariadb'
            ]
        },
        'netease': {
            'url': 'http://mirrors.cn99.com',
            'repositories': [
                'cpan', 'debian', 'gentoo gentoo/distfiles', 'mysql'
            ]
        },
        'tencent': {
            'url': 'https://mirrors.cloud.tencent.com',
            'repositories': [
                'apache', 'cpan CPAN', 'ctan CTAN', 'debian', 'gnu', 'libreoffice', 'mysql',
                'openbsd', 'postgresql', 'qt', 'videolan videolan-ftp', 'mariadb'
            ]
        },
        'heanet': {
            'url': 'http://heanet.dl.sourceforge.net',
            'repositories': [ 'sourceforge' ]
        }
    }

    @property
    def configuration(self) -> str:
        mirrors = {}
        for site in Mirrors_handler.preferred_sites:
            mirror_site = Mirrors_handler.mirror_sites[site]
            for repository in mirror_site['repositories']:
                path = repository.split(' ')[1] if len(repository.split(' ')) == 2 else repository.split(' ')[0]
                repository = repository.split(' ')[0]

                if (not repository in mirrors):
                    mirrors[repository] = [ repository ]
                    pass

                mirrors[repository].append(mirror_site['url'] + '/' + path)
                pass
            pass
        return '\n'.join(' '.join(mirror) for mirror in mirrors.values())

    pass
