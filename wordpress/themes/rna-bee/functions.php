<?php

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function rna_bee_enqueue_theme_assets() {
	$theme = wp_get_theme();

	wp_enqueue_style(
		'rna-bee-color-mode',
		get_stylesheet_directory_uri() . '/assets/css/color-mode.css',
		array(),
		$theme->get( 'Version' )
	);

	wp_enqueue_script(
		'rna-bee-color-mode',
		get_stylesheet_directory_uri() . '/assets/js/color-mode.js',
		array(),
		$theme->get( 'Version' ),
		true
	);
}
add_action( 'wp_enqueue_scripts', 'rna_bee_enqueue_theme_assets' );


function rna_bee_color_mode_bootstrap() {
	?>
	<script>
	(function () {
		try {
			var mode = localStorage.getItem('rna-bee-color-mode');

			if (mode !== 'light' && mode !== 'dark') {
				mode = window.matchMedia('(prefers-color-scheme: dark)').matches
					? 'dark'
					: 'light';
			}

			document.documentElement.dataset.colorMode = mode;
		} catch (e) {}
	})();
	</script>
	<?php
}
add_action( 'wp_head', 'rna_bee_color_mode_bootstrap', 1 );