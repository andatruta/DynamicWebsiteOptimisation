angular.module('dashboard').controller('analyticsController', ['$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {

	var ctrl = this;
	
	ctrl.versions = [
		{
			'title' : 'Version #1',
			'thumbnail' : 'static/dashboard/images/previews/version1.png'		
		},
		{
			'title' : 'Version #2',
			'thumbnail' : 'static/dashboard/images/previews/version2.png'		
		},
		{
			'title' : 'Version #3',
			'thumbnail' : 'static/dashboard/images/previews/version3.png'		
		},
		{
			'title' : 'Version #4',
			'thumbnail' : 'static/dashboard/images/previews/version4.png'		
		},
		{
			'title' : 'Version #5',
			'thumbnail' : 'static/dashboard/images/previews/version5.png'		
		},
	];

}]);