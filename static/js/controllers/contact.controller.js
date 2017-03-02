angular.module('app').controller('contactController', ['$scope', '$rootScope', '$window', function ($scope, $rootScope, $window) {

	var ctrl = this;

	ctrl.layout = $window.layoutType.layout;
	ctrl.fontSize = $window.layoutType.fontSize;
	
}]);