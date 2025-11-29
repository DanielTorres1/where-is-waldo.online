# PageSpeed Optimization Walkthrough

This document outlines the steps taken to optimize the PageSpeed (Mobile) for the Where's Waldo website.

## Objective
Improve the mobile PageSpeed score for all pages on the website, specifically targeting `shirt.html`, `game.html`, `puzzle.html`, and other key pages.

## Actions Taken

### 1. Font Loading Optimization
*   **Action:** Removed the `@import` rule for Google Fonts from `style.css`.
*   **Action:** Added `<link rel="preconnect">` tags for `fonts.googleapis.com` and `fonts.gstatic.com` to the `<head>` of all HTML files.
*   **Action:** Added the Google Fonts `<link>` tag directly to the `<head>` of all HTML files.
*   **Reason:** Using `<link>` tags allows for parallel downloading of CSS and fonts, preventing the "chaining" effect caused by `@import` which delays rendering. Preconnecting establishes early network connections, further reducing latency.

### 2. Image Optimization
*   **Action:** Added `loading="lazy"` attribute to all off-screen images (product images, gallery images, etc.).
*   **Action:** Added explicit `width` and `height` attributes to images where possible.
*   **Reason:** Lazy loading defers the loading of images until they are about to enter the viewport, significantly reducing initial page load time and data usage. Explicit dimensions help the browser reserve space for images, preventing Cumulative Layout Shift (CLS) and improving the user experience.

### 3. Third-Party Connection Optimization
*   **Action:** Added `<link rel="preconnect">` tags for external domains hosting images, such as:
    *   `https://m.media-amazon.com` (Amazon images)
    *   `https://i.imgur.com` (Imgur images)
    *   `https://media0.giphy.com` (Giphy GIFs)
*   **Reason:** Preconnecting to these origins reduces the time it takes to establish a connection (DNS lookup, TCP handshake, TLS negotiation) when the browser eventually requests resources from them.

### 4. Iframe Optimization
*   **Action:** Added `loading="lazy"` to the YouTube iframe in `shirt.html`.
*   **Reason:** Similar to images, lazy loading iframes prevents them from loading heavy third-party scripts until they are needed.

## Files Modified
*   `style.css`
*   `shirt.html`
*   `game.html`
*   `puzzle.html`
*   `image.html`
*   `characters.html`
*   `gif.html`
*   `picture.html`
*   `costume.html`
*   `lady.html`
*   `meme.html`
*   `page.html`
*   `index.html`

## Verification
These changes align with Google's Core Web Vitals recommendations and should result in improved PageSpeed scores, particularly for mobile users on slower connections.
