#!/bin/sh

set -eu

cd /var/www/html

echo "RNA-Bee WordPress bootstrap"
echo "=========================="

: "${WP_URL:?WP_URL is required}"
: "${WP_TITLE:?WP_TITLE is required}"
: "${WP_ADMIN_USER:?WP_ADMIN_USER is required}"
: "${WP_ADMIN_PASSWORD:?WP_ADMIN_PASSWORD is required}"
: "${WP_ADMIN_EMAIL:?WP_ADMIN_EMAIL is required}"

WP="wp --path=/var/www/html"


echo "Waiting for WordPress files..."

until [ -f /var/www/html/wp-config.php ]; do
    sleep 2
done


echo "WordPress files available."


#
# Install WordPress
#

if $WP core is-installed >/dev/null 2>&1; then
    echo "WordPress is already installed."
else
    echo "Installing WordPress..."

    $WP core install \
        --url="$WP_URL" \
        --title="$WP_TITLE" \
        --admin_user="$WP_ADMIN_USER" \
        --admin_password="$WP_ADMIN_PASSWORD" \
        --admin_email="$WP_ADMIN_EMAIL" \
        --skip-email

    echo "WordPress installed."
fi


#
# Site configuration
#

echo "Configuring site..."

$WP option update blogname "$WP_TITLE"
$WP option update timezone_string "Europe/Berlin"

$WP rewrite structure '/%postname%/'


#
# Make sure Twenty Twenty-Five exists
#

if $WP theme is-installed twentytwentyfive >/dev/null 2>&1; then
    echo "Twenty Twenty-Five is installed."
else
    echo "Installing Twenty Twenty-Five..."

    $WP theme install twentytwentyfive
fi


#
# Activate RNA-Bee child theme
#

if $WP theme is-active rna-bee >/dev/null 2>&1; then
    echo "RNA-Bee theme already active."
else
    echo "Activating RNA-Bee theme..."

    $WP theme activate rna-bee
fi


#
# Activate RNA-Bee plugin
#

if $WP plugin is-active rna-bee >/dev/null 2>&1; then
    echo "RNA-Bee plugin already active."
else
    echo "Activating RNA-Bee plugin..."

    $WP plugin activate rna-bee
fi


#
# Remove WordPress default content
#

delete_post_by_slug()
{
    TYPE="$1"
    SLUG="$2"

    IDS=$(
        $WP post list \
            --post_type="$TYPE" \
            --name="$SLUG" \
            --post_status=any \
            --format=ids
    )

    if [ -n "$IDS" ]; then
        echo "Removing default content: $SLUG"

        $WP post delete $IDS --force
    fi
}


delete_post_by_slug post hello-world
delete_post_by_slug page sample-page


#
# Helper: create page only when missing
#

get_page_id()
{
    SLUG="$1"

    $WP post list \
        --post_type=page \
        --name="$SLUG" \
        --post_status=any \
        --format=ids
}


#
# HOME
#

HOME_ID=$(get_page_id home)

if [ -z "$HOME_ID" ]; then

    echo "Creating Home page..."

    HOME_ID=$(
        $WP post create \
            --post_type=page \
            --post_status=publish \
            --post_title="RNA Bee" \
            --post_name="home" \
            --post_content='
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">RNA Bee</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Explore RNA structure, folding and computational evolution.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button -->
<div class="wp-block-button">
<a class="wp-block-button__link wp-element-button" href="/explore/">Start exploring</a>
</div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->
' \
            --porcelain
    )

else
    echo "Home page already exists: $HOME_ID"
fi


#
# ABOUT
#

ABOUT_ID=$(get_page_id about)

if [ -z "$ABOUT_ID" ]; then

    echo "Creating About page..."

    ABOUT_ID=$(
        $WP post create \
            --post_type=page \
            --post_status=publish \
            --post_title="About RNA Bee" \
            --post_name="about" \
            --post_content='
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">About RNA Bee</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>RNA Bee is an open-source experimental platform for computational RNA folding, mutation and evolution.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The project combines a WordPress interface with a Python and Django scientific backend.</p>
<!-- /wp:paragraph -->
' \
            --porcelain
    )

else
    echo "About page already exists: $ABOUT_ID"
fi


#
# EXPLORE
#

EXPLORE_ID=$(get_page_id explore)

if [ -z "$EXPLORE_ID" ]; then

    echo "Creating Explore page..."

    EXPLORE_ID=$(
        $WP post create \
            --post_type=page \
            --post_status=publish \
            --post_title="Explore" \
            --post_name="explore" \
            --post_content='
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Explore RNA Bee</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The interactive RNA-Bee experiments will live here.</p>
<!-- /wp:paragraph -->

<!-- wp:shortcode -->
[rna_bee]
<!-- /wp:shortcode -->
' \
            --porcelain
    )

else
    echo "Explore page already exists: $EXPLORE_ID"
fi


#
# Set static homepage
#

echo "Setting Home as front page..."

$WP option update show_on_front page
$WP option update page_on_front "$HOME_ID"


#
# Flush rewrites
#

$WP rewrite flush


echo
echo "================================="
echo "RNA-Bee WordPress bootstrap done."
echo "================================="
echo
echo "Home ID:    $HOME_ID"
echo "About ID:   $ABOUT_ID"
echo "Explore ID: $EXPLORE_ID"
echo
echo "Theme:"
$WP theme list --status=active
echo
echo "Plugins:"
$WP plugin list --status=active