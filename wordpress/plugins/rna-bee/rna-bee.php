<?php
/**
 * Plugin Name: RNA Bee
 * Description: WordPress presentation client for the RNA Bee Django REST API.
 * Version: 0.1.0
 * Author: Nathabee
 */

if (!defined('ABSPATH')) {
    exit;
}

function rna_bee_shortcode() {
    $api_url = esc_url(home_url('/api/'));
    return '<div id="rna-bee-app">'
         . '<h2>RNA Bee</h2>'
         . '<p>RNA simulation frontend skeleton.</p>'
         . '<p>API base: <code>' . $api_url . '</code></p>'
         . '</div>';
}

add_shortcode('rna_bee', 'rna_bee_shortcode');
