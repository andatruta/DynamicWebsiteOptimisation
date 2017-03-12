angular.module('dashboard').controller('createController', ['$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {

	var ctrl = this;

	ctrl.test = {
		'name': '',
		'descr': ''
	}

	ctrl.activeFeatures = [];

	console.log(ctrl.activeFeatures);

	ctrl.addFeature = function() {
		ctrl.activeFeatures.push({'name': '', 'variants': []});
		console.log(ctrl.activeFeatures);
	};

	ctrl.addVariant = function(featureIndex) {
		console.log("feature: " + featureIndex);
		ctrl.activeFeatures[featureIndex].variants.push({'name': ''});
		console.log(ctrl.activeFeatures);
	};

	ctrl.removeFeature = function(index) {
		ctrl.activeFeatures.splice(index, 1);
		console.log(ctrl.activeFeatures);
	};

	ctrl.removeVariant = function(featureIndex, variantIndex) {
		ctrl.activeFeatures[featureIndex].variants.splice(variantIndex, 1);
		console.log(ctrl.activeFeatures);
	};

}]);
