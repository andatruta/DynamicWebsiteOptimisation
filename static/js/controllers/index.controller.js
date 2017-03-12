angular.module('app').controller('indexController', ['$scope', '$rootScope', '$http', '$window', 'ALL_POSTS', function ($scope, $rootScope, $http, $window, allPosts) {

	var ctrl = this;

	ctrl.selectedPost = 'blog';

	console.log(ctrl.selectedPost);

	ctrl.layout = $window.layoutType.layout;
	ctrl.fontSize = $window.layoutType.fontSize;

	ctrl.posts = allPosts;

	ctrl.isSelected = function(post) {
		return ctrl.selectedPost == post;
	}

	ctrl.selectTab = function(post) {
		ctrl.selectedPost = post;
	}

	ctrl.registerClick = function(post) {
		// register click to DB
		$http({
                method: 'POST',
                url: '/registerClick'
            }).then(function(response) {
            	console.log(response)
            }, function(error) {
                console.log(error);
            });
        // set blog post to be displayed
        ctrl.selectTab(post);
	};

}]);