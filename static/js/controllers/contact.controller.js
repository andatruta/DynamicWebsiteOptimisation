angular.module('app').controller('contactController', ['$scope', '$rootScope', function ($scope, $rootScope) {

	var ctrl = this;

	ctrl.layout = $window.layoutType.layout;
	ctrl.fontSize = $window.layoutType.fontSize;
	
}]);