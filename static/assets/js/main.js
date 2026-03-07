/*
	Landed by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
	
	Modified: Disabled titleBar/navPanel injection and parallax on mobile (≤736px)
	to prevent conflicts with custom mobile bottom nav and top bar.
*/

(function($) {

	var $window = $(window),
		$body = $('body');

	// Detect mobile (≤736px) — matches your CSS breakpoint
	var isMobile = window.innerWidth <= 736;

	// Update on resize
	$window.on('resize', function() {
		isMobile = window.innerWidth <= 736;
	});

	// Breakpoints.
	breakpoints({
		xlarge: [ '1281px', '1680px' ],
		large:  [ '981px',  '1280px' ],
		medium: [ '737px',  '980px'  ],
		small:  [ '481px',  '736px'  ],
		xsmall: [ null,     '480px'  ]
	});

	// Play initial animations on page load.
	$window.on('load', function() {
		window.setTimeout(function() {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Touch mode.
	if (browser.mobile)
		$body.addClass('is-touch');

	// Scrolly links.
	$('.scrolly').scrolly({
		speed: 2000
	});

	// Dropdowns — desktop only.
	if (!isMobile) {
		$('#nav > ul').dropotron({
			alignment: 'right',
			hideDelay: 350
		});
	}

	// ── Nav: titleBar + navPanel ──
	// Only inject on desktop. On mobile we use #mobile-topbar + #bottom-nav instead.
	if (!isMobile) {
		// Title Bar.
		$(
			'<div id="titleBar">' +
				'<a href="#navPanel" class="toggle"></a>' +
				'<span class="title">' + $('#logo').html() + '</span>' +
			'</div>'
		).appendTo($body);

		// Panel.
		$(
			'<div id="navPanel">' +
				'<nav>' +
					$('#nav').navList() +
				'</nav>' +
			'</div>'
		)
		.appendTo($body)
		.panel({
			delay: 500,
			hideOnClick: true,
			hideOnSwipe: true,
			resetScroll: true,
			resetForms: true,
			side: 'left',
			target: $body,
			visibleClass: 'navPanel-visible'
		});
	}

	// ── Parallax ──
	// Disabled on IE, all mobile platforms, and our custom mobile breakpoint.
	if (browser.name == 'ie' || browser.mobile || isMobile) {

		$.fn._parallax = function() {
			return $(this);
		};

	} else {

		$.fn._parallax = function() {

			$(this).each(function() {

				var $this = $(this), on, off;

				on = function() {
					$this.css('background-position', 'center 0px');

					$window.on('scroll._parallax', function() {
						var pos = parseInt($window.scrollTop()) - parseInt($this.position().top);
						$this.css('background-position', 'center ' + (pos * -0.15) + 'px');
					});
				};

				off = function() {
					$this.css('background-position', '');
					$window.off('scroll._parallax');
				};

				breakpoints.on('<=medium', off);
				breakpoints.on('>medium', on);

			});

			return $(this);
		};

		$window.on('load resize', function() {
			$window.trigger('scroll');
		});

	}

	// ── Spotlights ──
	var $spotlights = $('.spotlight');

	$spotlights
		._parallax()
		.each(function() {

			var $this = $(this), on, off;

			on = function() {

				var top, bottom, mode;

				// Use main <img>'s src as spotlight background.
				$this.css('background-image', 'url("' + $this.find('.image.main > img').attr('src') + '")');

				if ($this.hasClass('top')) {
					mode = 'top';
					top = '-20%';
					bottom = 0;
				} else if ($this.hasClass('bottom')) {
					mode = 'bottom-only';
					top = 0;
					bottom = '20%';
				} else {
					mode = 'middle';
					top = 0;
					bottom = 0;
				}

				$this.scrollex({
					mode:       mode,
					top:        top,
					bottom:     bottom,
					initialize: function() { $this.addClass('inactive'); },
					terminate:  function() { $this.removeClass('inactive'); },
					enter:      function() { $this.removeClass('inactive'); },
				});
			};

			off = function() {
				$this.css('background-image', '');
				$this.unscrollex();
			};

			breakpoints.on('<=medium', off);
			breakpoints.on('>medium', on);

		});

	// ── Wrappers ──
	var $wrappers = $('.wrapper');

	$wrappers.each(function() {

		var $this = $(this), on, off;

		on = function() {
			$this.scrollex({
				top:        250,
				bottom:     0,
				initialize: function() { $this.addClass('inactive'); },
				terminate:  function() { $this.removeClass('inactive'); },
				enter:      function() { $this.removeClass('inactive'); },
			});
		};

		off = function() {
			$this.unscrollex();
		};

		breakpoints.on('<=medium', off);
		breakpoints.on('>medium', on);

	});

	// ── Banner ──
	var $banner = $('#banner');
	$banner._parallax();

})(jQuery);