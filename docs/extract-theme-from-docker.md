# extract child theme 


## extract child Theme and send in github
extract from rna.nathabee.de running in docker the change in a child of 2025 



Install Create Block Theme in that running Docker WordPress.
Use it to create a child theme from Twenty Twenty-Five.
Verify the child contains your palette, sticky header, no-title template, and any useful patterns.
Export/copy that child theme out of the container.
Put the child theme into your local Git repository.
Commit and push it.
Only after that, test a fresh installation from empty volumes


docker compose exec wordpress ls -la /var/www/html/wp-content/themes/rna-bee
mkdir -p wordpress/themes
docker compose cp   wordpress:/var/www/html/wp-content/themes/rna-bee   ./wordpress/themes/
find wordpress/themes/rna-bee -maxdepth 3 -type f
git status
git add wordpress/themes/rna-bee
git commit -m "Add RNA-Bee child theme"
git push

in lokal 
git pull





