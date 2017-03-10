'use strict';   // See note about 'use strict'; below

// BLOG APP

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

app.controller('mainController', ['$scope','$http', '$window', function ($scope, $http, $window) {
	$scope.rating = 5;

	$scope.rateFunction = function(rating) {
		console.log('Rating selected - ' + rating);
		// register rating 
		$http({
			method: 'POST',
			url: '/rating',
			data: {
				rating: rating,
				version: $window.layoutType
			}
		}).then(function successCallback(response) {
			// alert("Thank you for rating!");
			// Reload page after rating
			$window.location.reload();
		}, function errorCallback(response) {
			console.log(response);
		});
	};

	$scope.pages = [
		{
			'title': 'Home',
			'link': '#',
		},
		{
			'title': 'About',
			'link': '/#/about',
		},
		{
			'title': 'Contact',
			'link': '/#/contact',
		},
	];

	$scope.selectedLink = 0;

	$scope.selectLink = function(index) {
		console.log(index);
	   $scope.selectedLink = index; 
	};
}])
.directive('starRating', function() {
	return {
		restrict : 'A',
		template : '<ul class="rating">'
				 + '	<li ng-repeat="star in stars" ng-class="star" ng-click="toggle($index)">'
				 + '\u2605'
				 + '</li>'
				 + '</ul>',
		scope : {
			ratingValue : '=',
			max : '=',
			onRatingSelected : '&'
		},
		link : function(scope, elem, attrs) {
			var updateStars = function() {
				scope.stars = [];
				for ( var i = 0; i < scope.max; i++) {
					scope.stars.push({
						filled : i < scope.ratingValue
					});
				}
			};
			
			scope.toggle = function(index) {
				scope.ratingValue = index + 1;
				scope.onRatingSelected({
					rating : index + 1
				});
			};
			
			scope.$watch('ratingValue',
				function(oldVal, newVal) {
					if (newVal) {
						updateStars();
					}
				}
			);
		}
	};
});

// DASHBOARD APP

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
				templateUrl: 'static/dashboard/partials/index.html',
				controller: 'analyticsController',
				controllerAs: 'ctrl',
			}).
			when('/dashboard/create', {
				templateUrl: 'static/dashboard/partials/create.html',
				controller: 'createController',
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
				'link': '/dashboard',
				'icon': 'static/dashboard/images/icons/home-icon.png'
			},
			{
				'title': 'Create',
				'link': '/#/dashboard/create',
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
