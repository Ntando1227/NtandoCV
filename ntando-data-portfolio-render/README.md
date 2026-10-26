# Ntando Mtimkulu Data Portfolio

A self-contained static portfolio prepared for Git and Render deployment.

## What's included

- `dist/index.html`: portfolio homepage
- `dist/workbook-preview.html`: read-only workbook previews
- `dist/workbook-previews/images/`: worksheet preview images
- `dist/samples/`: editable Excel workbooks and supporting sample files
- `dist/ntando-mtimkulu-cv.pdf`: downloadable CV
- `render.yaml`: Render Blueprint for a static site

The site uses plain HTML, CSS and JavaScript. It has no package installation or compilation step. GPT Sites hosting metadata is not included.

## Commit the project to GitHub

Extract this folder, open a terminal in the extracted project folder, then run:

```sh
git init
git add .
git commit -m "Add Ntando Mtimkulu data portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ntando-data-portfolio.git
git push -u origin main
```

Replace the remote URL with the repository you created on GitHub.

## Deploy with Render Blueprint

1. Sign in to Render and choose **New** then **Blueprint**.
2. Connect the GitHub repository.
3. Render reads `render.yaml` and configures the static site.
4. Review the settings and deploy.

The Blueprint publishes the `dist` folder. Render can redeploy when new commits are pushed to the linked branch.

## Deploy as a static site manually

If you prefer not to use a Blueprint, create a new **Static Site** in Render and use:

- Build command: `echo "No build step required"`
- Publish directory: `dist`

## Updating the portfolio

Edit the files in `dist`, commit the changes and push them to the connected GitHub branch. Keep workbook preview image names and links in `dist/workbook-preview.html` aligned with the files in `dist/workbook-previews/images/` and `dist/samples/`.
