'use strict';   // See note about 'use strict'; below

var app = angular.module('app', [
 'ngRoute'
]);

app.config(['$locationProvider', function($locationProvider) {
	// $locationProvider.html5Mode(true);
	$locationProvider.hashPrefix('');
}]);


app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
			when('/', {
				templateUrl: 'static/partials/index.html',
				controller: 'indexController',
				controllerAs: 'ctrl',
			}).
			when('/about',  {
				templateUrl: 'static/partials/about.html',
				controller: 'aboutController',
				controllerAs: 'ctrl',
			}).
			when('/contact',  {
				templateUrl: 'static/partials/contact.html',
				controller: 'contactController',
				controllerAs: 'ctrl',
			}).
			otherwise({
				redirectTo: '/'
			});
	}
]);

var dashboard = angular.module('dashboard', [
 'ngRoute'
]);

dashboard.config(['$locationProvider', function($locationProvider) {
	$locationProvider.html5Mode(true);
	$locationProvider.hashPrefix('');
}]);

dashboard.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
			when('/dashboard', {
				templateUrl: 'static/dashboard/index.html',
				controller: 'analyticsController',
				controllerAs: 'ctrl',
			}).
			otherwise({
				redirectTo: '/dashboard'
			});
	}
]);

dashboard.controller('selectPage', function($scope) {

    $scope.pages = [
            {
                'title': 'Home',
                'link': '#',
                'icon': 'static/dashboard/images/icons/home-icon.png'
            },
            {
                'title': 'Create',
                'link': '/#/create',
                'icon': 'static/dashboard/images/icons/create-icon.png'

            },
            {
                'title': 'Analytics',
                'link': '/#/analytics',
                'icon': 'static/dashboard/images/icons/analytics-icon.png'
            },
            {
                'title': 'Settings',
                'link': '/#/settings',
                'icon': 'static/dashboard/images/icons/settings-icon.png'
            },
        ];

    $scope.selectedLink = 0;

    $scope.selectLink = function(index) {
    	console.log(index);
       $scope.selectedLink = index; 
    };
});

dashboard.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  }
});
