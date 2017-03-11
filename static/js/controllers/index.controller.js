angular.module('app').controller('indexController', ['$scope', '$rootScope', '$http', '$window', 'ALL_POSTS', function ($scope, $rootScope, $http, $window, allPosts) {

	var ctrl = this;

	ctrl.selectedPost = 'blog';

	console.log(ctrl.selectedPost);

	ctrl.layout = $window.layoutType.layout;
	ctrl.fontSize = $window.layoutType.fontSize;
	
	// ctrl.posts = [
	// 	{
	// 		'title' : 'Multi-objective multi-armed bandits',
	// 		'thumbnail' : 'static/images/pic01.jpg',
	// 		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
	// 		'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
	// 	},
	// 	{
	// 		'title' : 'Upper Confidence Bound algorithm',
	// 		'thumbnail' : 'static/images/pic02.jpg',
	// 		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
	// 		'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
	// 	},
	// 	{
	// 		'title' : 'Softmax algorithm',
	// 		'thumbnail' : 'static/images/pic03.jpg',
	// 		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
	// 		'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
	// 	},
	// 	{
	// 		'title' : 'Variations on the exploration rate',
	// 		'thumbnail' : 'static/images/pic04.jpg',
	// 		'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
	// 		'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
	// 	},
	// 	{
	// 		'title' : 'Initial E-greedy algorithm',
	// 		'thumbnail' : 'static/images/pic05.jpg',
	// 		'descr': '',
	// 		'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
	// 	}
	// ];
	ctrl.posts = allPosts;
	console.log(ctrl.posts);

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