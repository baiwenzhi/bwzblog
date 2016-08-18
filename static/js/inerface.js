var mainapp = angular.module("mainapp",['ngRoute','ngSanitize']);
    mainapp.config(function($routeProvider) {
    $routeProvider
        .when('/blogs', {
            templateUrl: '/static/templates/block/blogs.html',
            controller: 'blogsController'
        })
        .when('/blog/:blog_name',{
            templateUrl: '/static/templates/block/blog.html',
            controller: 'blogController'
        })
        .when('/category/:category_id',{
            templateUrl: '/static/templates/block/blogs.html',
            controller: 'blogsController'
        })
        .when('/search',{
            templateUrl: '/static/templates/block/blogs.html',
            controller: 'blogsController'
        })
        .when('/fav',{
            templateUrl: '/static/templates/block/blogs.html',
            controller: 'blogsController'
        })
        .when('/tag/:tag_id',{
            templateUrl: '/static/templates/block/blogs.html',
            controller: 'blogsController'
        })
        .when('/timeline',{
            templateUrl: '/static/templates/block/timeline.html',
            controller: 'timelineController'
        })
    .otherwise({
        redirectTo: '/blogs'
      });
});
mainapp.run(function($rootScope, $location){
$rootScope.$on('$routeChangeStart', function(evt, next, current){
Top()
  });
})
mainapp.factory('fac_page_active',function($rootScope){
    var tars = {}
    tars.active_page='';
    tars.menu_active=false;
    tars.categorymenu_style={};
    tars.update_active_page = function(pagename){
        tars.active_page = pagename
        $rootScope.$broadcast('pagechange');
    }
    tars.update_menu_active = function(){
        tars.menu_active = !tars.menu_active
        $rootScope.$broadcast('menuchange');
    }
    return tars
});
mainapp.filter('to_trusted', ['$sce', function ($sce) {
        return function (text) {
            return $sce.trustAsHtml(text);
        }
    }
]);
mainapp.directive('color',function(){
    var color = function(m,s,c){
        return (c ? arguments.callee(m,s,c-1) : '#') +
          s[m.floor(m.random() * 16)]
      }
    return {
        restrict : 'EA',
        link : function(scope, element, attrs) {
            element.attr('style','background:'+color(Math,'0123456789abcdef',5))
        }
    }
});
mainapp.directive('paging',function(){
    return {
        replace:true,
        controller:function($scope,$element,$location){
            var pageno = parseInt($location.search().page||1)
            var maxpage = Math.ceil($scope.count/10)
            var str="<ul>"
            if ($scope.previous){
                str+='<li><a href="#'+$scope.previous.replace("http://"+window.location.host+"/api",'')+'">上一页</a></li>'
            }
            for(var i= 1;i<=maxpage;i++){
                var searchs = $location.search()
                searchs.page = i
                var url=$location.path()
                for ( var k in searchs ){
                    if (url == $location.path()){
                        url +="?"+k+"="+searchs[k]
                    }else{
                        url+="&"+k+"="+searchs[k]
                    }

                }
                if(i == pageno){
                    str+='<li class="active"><a href="#'+url+'">'+i+'</a></li>'
                }else{
                    str+='<li><a href="#'+url+'">'+i+'</a></li>'
                }
            }
            if($scope.next){
                str+='<li><a href="#'+$scope.next.replace("http://"+window.location.host+"/api",'')+'">下一页</a></li>'
            }
            $element.html(str);
        }

    }
})
mainapp.controller("menuController",function($scope,$http,fac_page_active){
    $scope.categorys=[]
    $scope.menu_active=fac_page_active.menu_active;;
    $scope.active_page=fac_page_active.active_page;
    $scope.categorymenu_style=fac_page_active.categorymenu_style;

    if (sessionStorage.getItem('categorys')){
        $scope.categorys = JSON.parse(sessionStorage.getItem('categorys'));
    }else{
        $http.get('/api/categorys',{cache:true}).success(function(data, status, headers, config) {
            sessionStorage.setItem('categorys',JSON.stringify(data))
            $scope.categorys = data;
        });
    }
    $scope.o_c_categorys=function(){
        $scope.menu_active=!$scope.menu_active
        if($scope.menu_active){
            $scope.categorymenu_style={
                "height":$scope.categorys.length*39+'px'
            }
        }else{
            $scope.categorymenu_style={}
        }
    }
    $scope.active = function(menu){
        window.scrollTo(0,0)
        $scope.active_page=menu
    }
    $scope.$on('pagechange',function(){
        $scope.active_page=fac_page_active.active_page
    })
    $scope.$on('menuchange',function(){
        $scope.menu_active=fac_page_active.menu_active
        if($scope.menu_active){
            $scope.categorymenu_style={
                "height":$scope.categorys.length*39+'px'
            }
        }
    })
});
mainapp.controller("blogsController",function($scope,$http,$location,$filter,fac_page_active){
    $scope.count=0
    $scope.next=''
    $scope.previous=''
    $scope.blogs=''
    $scope.loadingend = false;
    fac_page_active.update_active_page($location.path().replace('/',''))
    if ($location.url().indexOf('category')!=-1&&fac_page_active.menu_active==false){
        fac_page_active.update_menu_active()
    }
    var promise = $http.get('/api'+$location.url(),{cache:true}).success(function(data, status, headers, config) {
        $scope.blogs = data.results;
        $scope.count=data.count
        $scope.next=data.next
        $scope.previous=data.previous
     });
    promise.then(function(){
        $scope.loadingend=true
    })

    $scope.goto=function(url){
        window.scrollTo(0,0)
        var tr = url.replace("http://"+window.location.host+"/api",'')
        $location.url(tr)
    }
});
mainapp.controller("blogController",function($scope,$http,$routeParams){
    $scope.loadingend = false;

    var url = '/api/blog/'+$routeParams.blog_name
    var promise = $http.get(url,{cache:true}).success(function(data, status, headers, config) {
        $scope.blog = data;
     });

    promise.then(function(){
        $scope.loadingend = true;
        var dodo = function(){
            var el = document.createElement('div');//该div不需要设置class="ds-thread"
            el.setAttribute('data-thread-key', $scope.blog.id);//必选参数
            el.setAttribute('data-url', "http://www.baiwenzhi.com/#/blog/"+$scope.blog.name)//必选参数
            DUOSHUO.EmbedThread(el);
            document.getElementById('duoshuocontent').appendChild(el)
        }
        setTimeout(dodo,100)
    })
});
mainapp.controller("timelineController",function($scope,$http,$location,fac_page_active){
    $scope.count=0
    $scope.loadingend = false;
    fac_page_active.update_active_page('timeline')
    $http.get('/api'+$location.url(),{cache:true}).success(function(data, status, headers, config) {
        $scope.blogs = data
        $scope.loadingend = true;
     });
});

angular.bootstrap(document,['mainapp']);
function Top(){
    window.scrollTo(0,0)
}

function search(){
    if(document.getElementById('search_keywords').value!=''){
        var url = '/#/search/?keywords='+document.getElementById('search_keywords').value

        window.location.href=url
    }
}