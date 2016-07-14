'use strict';
require.config({
    //配置angular的路径
    paths:{
        "angular":"angular.min",
        "angular-route":"angular-route",
        "ng-sanitize":"sanitize"
    },
    //这个配置是你在引入依赖的时候的包名
    shim:{
        "angular":{
            exports:"angular"
        },
        "angular-route":{
            exports:"angular-route"
        },
        "ng-sanitize":{
            exports:"ng-sanitize"
        }
    }
})

define(["angular","angular-route","ng-sanitize"],function(angular){

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
    mainapp.controller("menuController",function($scope,$http,fac_page_active){
        $scope.categorys=[]
        $scope.menu_active=fac_page_active.menu_active;;
        $scope.active_page=fac_page_active.active_page;
        $scope.categorymenu_style=fac_page_active.categorymenu_style;

        if (localStorage.getItem('categorys')){
            $scope.categorys = JSON.parse(localStorage.getItem('categorys'));
        }else{
            $http.get('/api/categorys').success(function(data, status, headers, config) {
                localStorage.setItem('categorys',JSON.stringify(data))
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
        $scope.keywords=''
        $scope.words=''
        fac_page_active.update_active_page($location.path().replace('/',''))
        if ($location.path().indexOf('category')!=-1&&fac_page_active.menu_active==false){
            fac_page_active.update_menu_active()
        }
        var promise = $http.get('/api'+$location.path()).success(function(data, status, headers, config) {
            $scope.blogs = data.results;
         });
        $scope.search = function(){
            $scope.keywords=$scope.words
        }
        promise.then(function(){
            var dodo = function(){
                SyntaxHighlighter.highlight();
            }
            setTimeout(dodo,100)
        })
    });
    mainapp.controller("blogController",function($scope,$http,$routeParams){
        var url = '/api/blog/'+$routeParams.blog_name
        var promise = $http.get(url).success(function(data, status, headers, config) {
            $scope.blog = data;
         });

        promise.then(function(){
            var dodo = function(){
                SyntaxHighlighter.highlight();
                var el = document.createElement('div');//该div不需要设置class="ds-thread"
                el.setAttribute('data-thread-key', $scope.blog.id);//必选参数
                el.setAttribute('data-url', "http://www.baiwenzhi.com/#/blog/"+$scope.blog.name)//必选参数
                DUOSHUO.EmbedThread(el);
                document.getElementById('duoshuocontent').appendChild(el)
            }
            setTimeout(dodo,100)
        })
    });
    mainapp.controller("timelineController",function($scope,$http,fac_page_active){
        fac_page_active.update_active_page('timeline')
        $http.get('/api/timeline').success(function(data, status, headers, config) {

          $scope.blogs = data.results;

         });
    });

    angular.bootstrap(document,['mainapp']);
})
function Top(){
    window.scrollTo(0,0)
}