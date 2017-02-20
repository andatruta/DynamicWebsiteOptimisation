angular.module('app').controller('indexController', ['$scope', '$rootScope', '$http', '$window', function ($scope, $rootScope, $http, $window) {

	var ctrl = this;

	ctrl.selectedPost = 'blog';

	console.log(ctrl.selectedPost);

	ctrl.layout = $window.layoutType.layout;
	ctrl.fontSize = $window.layoutType.fontSize;
	
	ctrl.posts = [
		{
			'title' : 'Blog post #1',
			'thumbnail' : 'static/images/pic01.jpg',
			'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
			'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
		},
		{
			'title' : 'Blog post #2',
			'thumbnail' : 'static/images/pic02.jpg',
			'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
			'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
		},
		{
			'title' : 'Blog post #3',
			'thumbnail' : 'static/images/pic03.jpg',
			'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
			'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
		},
		{
			'title' : 'Blog post #4',
			'thumbnail' : 'static/images/pic04.jpg',
			'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
			'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
		},
		{
			'title' : 'Blog post #5',
			'thumbnail' : 'static/images/pic05.jpg',
			'descr': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.',
			'content': 'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.' 
		}
	];

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