"""
Will be having the test data which will be used in feeds app test cases
"""
from datetime import timedelta

from django.utils import timezone

VALID_RSS_FEED_DATA = '<?xml version="1.0" encoding="UTF-8"?>\n<feed xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">' \
                      '\n  <id>tag:blog.svbtle.com,2014:/feed</id>\n  <link rel="alternate" type="text/html"' \
                      ' href="http://blog.svbtle.com"/>\n  <link rel="self" type="application/atom+xml" ' \
                      'href="http://blog.svbtle.com/feed"/>\n  <title>Svbtle Blog</title>\n  ' \
                      '<updated>2016-02-29T13:05:24-08:00</updated>\n  <author>\n    ' \
                      '<name>Svbtle Network</name>\n    <uri>http://blog.svbtle.com</uri>\n   ' \
                      ' <email>hello@svbtle.com</email>\n  </author>\n  <generator>Svbtle.com</generator>\n  <entry>\n   ' \
                      ' <id>tag:blog.svbtle.com,2014:Post/svbtle-promise</id>\n    ' \
                      '<published>2016-02-29T13:05:24-08:00</published>\n    ' \
                      '<updated>2016-02-29T13:05:24-08:00</updated>\n    ' \
                      '<link rel="alternate" type="text/html" href="http://blog.svbtle.com/svbtle-promise"/>\n    ' \
                      '<title>The Svbtle Promise</title>\n    ' \
                      '<content type="html">&lt;p&gt;&lt;span style="font-style: italic; font-family: Georgia; ' \
                      'font-size: 14px;"&gt;By&lt;/span&gt; &lt;a href="http://dcurt.is"&gt;&lt;span ' \
                      'style="letter-spacing: 1px; color: #1d1d1d; font-family: freight-sans-pro; font-weight: 900; ' \
                      'font-size: 18px;"&gt;DUSTIN CURTIS&lt;/span&gt;&lt;/a&gt;&lt;/p&gt;\n\n' \
                      '&lt;p&gt;Today, we&amp;rsquo;re launching a new feature for Svbtle members: it&amp;' \
                      'rsquo;s a promise that the Svbtle service and your published content will remain available ' \
                      'on the web forever. You can read the details here: &lt;' \
                      'a href="https://svbtle.com/promise"&gt;Svbtle Promise &amp;rarr;&lt;/a&gt;&lt;/p&gt;' \
                      '\n\n&lt;p&gt;For more information, read the announcement &lt;' \
                      'a href="http://dcurt.is/svbtle-promise"&gt;here, on Dustin Curtis&amp;rsquo; blog&lt;' \
                      '/a&gt;.&lt;/p&gt;\n</content>\n  </entry>\n  <entry>\n    ' \
                      '<id>tag:blog.svbtle.com,2014:Post/open-for-everyone</id>\n    ' \
                      '<published>2014-01-28T09:36:03-08:00</published>\n    ' \
                      '<updated>2014-01-28T09:36:03-08:00</updated>\n    ' \
                      '<link rel="alternate" type="text/html" href="http://blog.svbtle.com/open-for-everyone"/>\n    ' \
                      '<title>Open for everyone</title>\n    ' \
                      '<content type="html">&lt;p&gt;&lt;span style="font-style: italic; ' \
                      'font-family: Georgia; font-size: 14px;"&gt;By&lt;/span&gt; &lt;a href="http://dcurt.is"&gt;&lt;' \
                      'span style="letter-spacing: 1px; color: #1d1d1d; font-family: freight-sans-pro; font-weight: 900; ' \
                      'font-size: 18px;"&gt;DUSTIN CURTIS&lt;/span&gt;&lt;/a&gt;&lt;/p&gt;\n\n&lt;p&gt;' \
                      'When I first started working on Svbtle, I was building it out of frustration. ' \
                      'I felt that publishing platforms had become too complicated by focusing on the wrong things. ' \
                      'What I was looking for was a platform that rolled up its sleeves and worked hard to get at ' \
                      'the core of what writing is really about&amp;ndash;sharing ideas, naturally.&lt;/p&gt;' \
                      '\n\n&lt;p&gt;Svbtle is designed to highlight the things that matter; ' \
                      'it&amp;rsquo;s an extremely simple platform for collecting and developing ideas, ' \
                      'sharing them with the world, and reading them. That&amp;rsquo;s it. We&amp;rsquo;' \
                      've focused all of our energy into designing the simplest interface possible for ' \
                      'accomplishing these goals. Svbtle is blogging with everything else stripped away.&lt;' \
                      '/p&gt;\n\n&lt;p&gt;Until now, we&amp;rsquo;ve been an exclusive platform open only to ' \
                      'approved users. We took this initial approach because we wanted to ensure that the software' \
                      ' worked, first of all, and that the platform was seeded with great content by seasoned and ' \
                      'experienced authors. Now we&amp;rsquo;re finally ready to let more people try Svbtle. ' \
                      'Today, &lt;a href="https://svbtle.com/signup"&gt;we&amp;rsquo;re opening sign up for ' \
                      'everyone&lt;/a&gt;.&lt;/p&gt;\n\n&lt;hr&gt;\n&lt;h1 id="why-use-svbtle_1"&gt;&lt;' \
                      'a class="head_anchor" href="#why-use-svbtle_1"&gt;&amp;nbsp;&lt;/a&gt;Why ' \
                      'use Svbtle?&lt;/h1&gt;\n&lt;p&gt;&lt;strong&gt;It works like your brain.&lt;' \
                      '/strong&gt;&lt;br /&gt; Svbtle\xe2\x80\x99s dashboard is designed to work ' \
                      'the same way your brain works. It encourages you to dump ideas, links, and thoughts into' \
                      ' a flow of draft posts, and then makes it easy to slowly sculpt those ideas into publishable' \
                      ' articles. It just feels natural. &lt;br /&gt; &lt;br&gt;\n&lt;' \
                      'a href="https://svbtleusercontent.com/x7rg26fs3udzxa.png"&gt;&lt;' \
                      'img src="https://svbtleusercontent.com/x7rg26fs3udzxa_small.png" ' \
                      'alt="svbtle_interface.png"&gt;&lt;/a&gt;&lt;/p&gt;\n\n&lt;p&gt;&lt;strong&gt;' \
                      'It gets out of the way.&lt;/strong&gt;&lt;br /&gt; When we\xe2\x80\x99re writing, ' \
                      'we like to have no distractions, so we removed all of them. Only a few essential styling ' \
                      'options remain, but articles can be written using shorthand formatting with &lt;' \
                      'a href="http://daringfireball.net/projects/markdown/"&gt;Markdown&lt;/a&gt;, for more control. ' \
                      '(Don\xe2\x80\x99t worry; it\xe2\x80\x99s easy to learn.)&lt;' \
                      '/p&gt;\n\n&lt;p&gt;Svbtle\xe2\x80\x99s writing interface was designed to get out of the way, ' \
                      'and it lets you focus on writing. &lt;br /&gt; &lt;br&gt;\n&lt;' \
                      'a href="https://svbtleusercontent.com/hpzgmmskxrba.png"&gt;&lt;' \
                      'img src="https://svbtleusercontent.com/hpzgmmskxrba_small.png" alt="write.png"&gt;&lt;' \
                      '/a&gt;&lt;/p&gt;\n\n&lt;p&gt;&lt;strong&gt;It cares about your identity.&lt;/strong&gt;&lt;' \
                      'br /&gt; Writers shouldn\xe2\x80\x99t be defined by the brands of their publishers or platform, ' \
                      'but rather by their own personal presence on the web. So we\xe2\x80\x99ve built features that ' \
                      'enable you to own your space inside Svbtle: Your full name appears by everything you write,' \
                      ' you can use a custom domain, and you can choose an avatar and accent color. We have plans for' \
                      ' more personalization and branding features soon, too.&lt;/p&gt;\n\n&lt;hr&gt;\n\n&lt;p&gt;' \
                      'We want to make the best place for writing, reading, and building a personal presence on the web.' \
                      ' And we&amp;rsquo;re just getting started. Give Svbtle a try; I hope you enjoy what we&amp;' \
                      'rsquo;ve built.&lt;/p&gt;\n\n&lt;p&gt;&lt;span style="font-size: 25px; font-weight: 500;' \
                      '"&gt;&lt;a href="https://svbtle.com/signup" style="font-weight: 800;"&gt;Sign up &amp;rarr;' \
                      '&lt;/a&gt;&lt;/span&gt;&lt;/p&gt;\n</content>\n  </entry>\n  <entry>\n    <id>' \
                      'tag:blog.svbtle.com,2014:Post/hello-world</id>\n    ' \
                      '<published>2012-06-08T14:28:00-07:00</published>\n    <updated>2012-06-08T14:28:00-07:00</updated>' \
                      '\n    <link rel="alternate" type="text/html" href="http://blog.svbtle.com/hello-world"/>\n    ' \
                      '<title>Hello, world!</title>\n    <content type="html">&lt;p&gt;This is the Official Svbtle Blog.' \
                      ' It&amp;rsquo;ll be updated with information about members and features of the Svbtle Network. ' \
                      '&lt;/p&gt;\n\n&lt;p&gt;Want to apply for membership? &lt;a href="http://svbtle.com/apply"&gt;Do ' \
                      'it here.&lt;/a&gt;&lt;/p&gt;\n</content>\n  </entry>\n</feed>\n'


INVALID_RSS_FEED_DATA = '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  ' \
                        '<script>var _sf_startpt=(new Date()).getTime()</script>\n  <title>Svbtle Blog</title>\n  ' \
                        '<script>(function(d) {var config = {kitId: \'tze3uwp\',scriptTimeout: 1000,async: true},' \
                        'h=d.documentElement,t=setTimeout(function()' \
                        '{h.className=h.className.replace(/\\bwf-loading\\b/g,"")+" wf-inactive";},' \
                        'config.scriptTimeout),tk=d.createElement("script"),' \
                        'f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";' \
                        'tk.src=\'https://use.typekit.net/\'+config.kitId+\'.js\';tk.async=true;' \
                        'tk.onload=tk.onreadystatechange=function(){a=this.readyState;' \
                        'if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}' \
                        'catch(e){}};s.parentNode.insertBefore(tk,s)})(document);</script>\n  ' \
                        '<meta name="viewport" content="width=device-width, initial-scale=1">\n ' \
                        ' <link rel="shortcut icon" ' \
                        'href="https://d1yg14i6wd46hx.cloudfront.net/assets/' \
                        'favicon-5ed3591b57f6a4f0d5cb82c6680b33bb1058fe757c71ccb094952824e7e00b17.ico">\n ' \
                        ' <meta name="generator" content="Svbtle.com" />\n  <meta name="description" content="Svbtle Blog' \
                        ' | A blogging platform"/>\n  <link rel="canonical" href="http://blog.svbtle.com" />\n  ' \
                        '<meta name="og:url" content="http://blog.svbtle.com" />\n  ' \
                        '<meta property="twitter:card" content="summary" />\n  <meta property="twitter:site" ' \
                        'content="@svbtle" />\n  <meta property="twitter:title" content="Svbtle Blog" />\n  ' \
                        '<meta property="twitter:description" content="Svbtle Blog | A blogging platform" />\n ' \
                        ' <meta property="twitter:creator" content="@svbtle" />\n  <meta property="twitter:image:src" ' \
                        'content="https://d2l2xugcou6irs.cloudfront.net/svbtle_logo.png" />\n  ' \
                        '<meta property="twitter:domain" content="http://blog.svbtle.com" />\n  ' \
                        '<meta property="og:title" content="Svbtle Blog on Svbtle" />\n ' \
                        ' <meta property="og:type" content="blog" />\n  <meta property="og:description"' \
                        ' content="Svbtle Blog | A blogging platform" />\n  <meta property="og:image" ' \
                        'content="https://d2l2xugcou6irs.cloudfront.net/svbtle_logo.png" />\n  ' \
                        '<meta property="og:site_name" content="Svbtle Blog on Svbtle" />\n  ' \
                        '<meta property="fb:app_id" content="346346195413177" />\n\n  ' \
                        '<link rel="alternate" type="application/rss+xml" href="http://blog.svbtle.com/feed" />\n  ' \
                        '<link rel="stylesheet" media="all" ' \
                        'href="https://d1yg14i6wd46hx.cloudfront.net/assets/' \
                        'build.blog-db4b673480e6e3b28ec4a1249a28f8a4004f3e3ca4c9ee1613b7008c7a62b003.css" data-turbolinks-track="reload" />\n ' \
                        ' <script src="https://d1yg14i6wd46hx.cloudfront.net/assets/' \
                        'build.blog-5f5a64fb94eeb9405259946dc7a90f2c1abf3e373da6653a15ab1a82068736a2.js" data-turbolinks-track="reload">' \
                        '</script>\n <script>\n  (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){\n ' \
                        ' (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n  m=s.getElementsByTagName(o)[0];' \
                        'a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n  })(window,document,\'script\',\'//www.google-analytics.com/' \
                        'analytics.js\',\'ga\');\n  ga(\'create\', \'UA-41994323-1\');\n  ga(\'send\', \'pageview\');\n  </script>\n' \
                        '</head>\n<body class="overlord blog">\n<style scoped>\nfigure#user_logo a,\nfigure#user_foot a,\nfigure.avatar a,' \
                        '\nnav#overlord.user_top figure#logo_top a,\nfigure.kudo.complete div.filling {\n  background-image: ' \
                        'url(\'https://d1jcp5e5r52ocf.cloudfront.net/svbtle.png\')\n}\n\nfigure.kudo.activated div.filling,' \
                        '\nfigure.kudo.complete div.filling {\n  background-color: #000000;\n}\n\nfigure.kudo.activated a,' \
                        '\nfigure.kudo.complete a {\n  border-color: #000000;\n}\n\nblockquote,\na blockquote,\ndiv#readnext:hover ' \
                        'span.flank_title,\ndiv#foot_more:hover a,\ndiv#foot_userbar a#bottom_tagline span:hover,\narticle.linked ' \
                        'h1.article_title a:hover,\na.continue_button:hover,\narticle p a:hover,\nul#lightning_drop,\nfigure#user_logo,' \
                        '\nfigure#user_foot,\nul#user_links li a:hover,\nul#foot_links li a:hover,\na.buttonize:hover,' \
                        '\nbutton.buttonize:hover,\na.buttonize.outline:hover,\nbutton.buttonize.outline:hover,\nnav.pagination ' \
                        'span.next a:hover,\nnav.pagination span.prev a:hover,\nsection#readnext:hover p span,\nnav#overlord.user_top ' \
                        'figure#logo_top {\n  border-color: #000000;\n}\n\nfigure.avatar,\nnav#overlord.user_top figure#logo_top a,' \
                        '\nul#user_links li a:hover,\nul#foot_links li a:hover,\na.buttonize:hover,\nbutton.buttonize:hover,' \
                        '\na.buttonize.outline:hover,\nbutton.buttonize.outline:hover,\nnav.pagination span.next a:hover,' \
                        '\nnav.pagination span.prev a:hover,\nfigure#user_logo a,\nfigure#user_foot a  {\n\tbackground-color: #000000;\n}' \
                        '\n\nh6.separator_title.read_first,\nheader#user_top h2 a,\nfooter#blog_foot h5 a,\narticle.post h1 a:hover,' \
                        '\ndiv.preview strong,\nnav#overlord h2#nav_title.user_top a,\nsection#readnext:hover h3,' \
                        '\nsection#readnext:hover p span {\n  color: #000000;\n}\n\n@keyframes titlePulse\n  {\n  0% ' \
                        '{\n    color: #000000;\n  }\n  50% {\n    color: #000000;\n  }\n  100% {\n    color: #000000;\n  }\n}' \
                        '\n\n@-moz-keyframes titlePulse\n  {\n  0% {\n    color: #000000;\n  }\n  50% {\n    color: #000000;\n  }\n  100% ' \
                        '{\n    color: #000000;\n  }\n}\n\n@-webkit-keyframes titlePulse\n  {\n  0% {\n    color: #000000;\n  }\n  50% ' \
                        '{\n    color: #000000;\n  }\n  100% {\n    color: #000000;\n  }\n}\n\n\n</style>\n\n<figure id="loading">&nbsp;' \
                        '</figure>\n<nav id="overlord" class="">\n  <figure id="logo_top" class="">\n    <a href="/">Svbtle</a>\n  ' \
                        '</figure>\n  <figure id="hamburger">\n    <a href="#menu" id="hamburger_button">Menu</a>\n  </figure>\n ' \
                        ' <ul id="dropdown" class="onblog">\n    <li class="dropdown_message">\n     ' \
                        '<a href="https://svbtle.com">Svbtle Blog is writing on the <span class="logoize">Svbtle</span> network.</a>\n   ' \
                        ' </li>\n    <li><a href="https://twitter.com/svbtle">@svbtle</a></li>\n   ' \
                        ' <li><a href="http://svbtle.com"  target="_blank">svbtle.com</a></li>\n    ' \
                        '<li><a href="mailto:hello@svbtle.com?subject=hi%20from%20svbtle">say&nbsp;hello</a></li>\n    ' \
                        '<li><a href="/feed">rss feed</a></li>\n    <li style="margin: 0; padding: 0;"><hr class="overlord_nav" /></li>\n   ' \
                        ' <li><a href="https://svbtle.com/about">about svbtle</a></li>\n    ' \
                        '<li><a href="https://svbtle.com/signup">sign up</a></li>\n  </ul>\n</nav>\n<div id="whiteout"></div>' \
                        '\n\n<header id="user_top" class="cf ">\n  <figure id="user_logo"><a href="//blog.svbtle.com">Svbtle Blog</a>' \
                        '</figure>\n  <h2><a href="//blog.svbtle.com">Svbtle Blog</a></h2>\n  <h4>' \
                        '<span class="name_head">by</span> Svbtle Network</h4>\n  <h3>A blogging platform\n</h3>\n  ' \
                        '<ul id="user_links">\n    <li><a href="https://twitter.com/svbtle">@svbtle</a></li>\n    ' \
                        '<li><a href="mailto:hello@svbtle.com?subject=Svbtle">say hi</a></li>\n    ' \
                        '<li><a href="http://svbtle.com" >svbtle.com</a></li>\n  </ul>\n</header>\n' \
                        '<section id="container" class="blog user_home">\n  <h6 class="separator_title read_first">Read&nbsp;' \
                        'this&nbsp;first</h6>\n  <article id="mem3XeqTngsl8ViMbEWF" class="post user_show">\n    ' \
                        '<h1 class="article_title">\n      <a href="//blog.svbtle.com/svbtle-promise">The Svbtle Promise</a>\n ' \
                        '   </h1>\n    <a href="//blog.svbtle.com/svbtle-promise"><p><span style="font-style: italic; font-family: ' \
                        'Georgia; font-size: 14px;">By</span> <span style="letter-spacing: 1px; color: #1d1d1d; font-family: ' \
                        'freight-sans-pro; font-weight: 900; font-size: 18px;">DUSTIN CURTIS</span></p>\n\n<p>Today,' \
                        ' we\xe2\x80\x99re launching a new feature for Svbtle members: it\xe2\x80\x99s a promise that the Svbtle service ' \
                        'and your published content will remain available on the web forever. You can read the details here: Svbtle ' \
                        'Promise \xe2\x86\x92</p>\n\n<p>For more information, read the announcement here, on Dustin Curtis\xe2\x80\x99' \
                        ' blog.</p>\n</a>\n    <p><a href="//blog.svbtle.com/svbtle-promise" class="buttonize outline small">Continue' \
                        ' reading &rarr;</a></p>\n  </article>\n  <hr class="articlesplit" />\n  <article id="qDlB93NStdVfLIEEFlM"' \
                        ' class="post user_show">\n    <time datetime="2014-01-28" class="article_time">Jan 28, 2014</time>\n    ' \
                        '<h1 class="article_title"><a href="//blog.svbtle.com/open-for-everyone">Open for everyone</a></h1>\n    ' \
                        '<a href="//blog.svbtle.com/open-for-everyone" class="content"><p><span style="font-style: italic; font-family: ' \
                        'Georgia; font-size: 14px;">By</span> <span style="letter-spacing: 1px; color: #1d1d1d; font-family: ' \
                        'freight-sans-pro; font-weight: 900; font-size: 18px;">DUSTIN CURTIS</span></p>\n<p>When I first started working ' \
                        'on Svbtle, I was building it out of frustration. I felt that publishing platforms had become too ' \
                        'complicated by focusing on the wrong things. What I was looking for was a platform that rolled up its' \
                        ' sleeves and worked hard to get at the core of what writing is really about\xe2\x80\x93sharing ideas, naturally.</p>' \
                        '\n\n<p>Svbtle is designed to highlight the things that matter; it\xe2\x80\x99s an extremely' \
                        ' simple platform for collecting and developing ideas, sharing them with the world, and reading them. ' \
                        'That\xe2\x80\x99s it. We\xe2\x80\x99ve focused all of our energy into designing the simplest interface possible ' \
                        'for accomplishing these goals. Svbtle is blogging with everything else stripped away.</p>\n\n<p>Until now, ' \
                        'we\xe2\x80\x99ve been an exclusive platform open only to approved users. We took this initial approach because ' \
                        'we wanted to ensure that the software worked, first of all, and that the platform was</p></a>\n    ' \
                        '<p class="continue_mark"><a href="//blog.svbtle.com/open-for-everyone" class="buttonize outline small">' \
                        'Continue reading &rarr;</a></p>\n  </article>\n  <hr class="articlesplit" />\n  ' \
                        '<article id="joMLoN7121NzujLbiuC" class="post user_show">\n    ' \
                        '<time datetime="2012-06-08" class="article_time">Jun  8, 2012</time>\n    ' \
                        '<h1 class="article_title"><a href="//blog.svbtle.com/hello-world">Hello, world!</a></h1>\n    ' \
                        '<a href="//blog.svbtle.com/hello-world" class="content"><p>This is the Official Svbtle Blog.' \
                        ' It\xe2\x80\x99ll be updated with information about members and features of the Svbtle Network. </p>\n\n<p>' \
                        'Want to apply for membership? Do it here.</p>\n</a>\n    <p class="continue_mark">' \
                        '<a href="//blog.svbtle.com/hello-world" class="buttonize outline small">Continue reading &rarr;</a></p>\n  ' \
                        '</article>\n</section>\n<section id="subscribe" class="cf">\n  <p class="title">Subscribe to Svbtle Blog</p>\n  ' \
                        '<form class="new_blog_subscription" id="new_blog_subscription" action="/blog_subscriptions" ' \
                        'accept-charset="UTF-8" data-remote="true" method="post"><input name="utf8" type="hidden" value="&#x2713;" />\n    ' \
                        '<div class="input_box cf">\n    <input placeholder="What&#39;s your email?" class="pane_input" type="email" ' \
                        'name="blog_subscription[email]" id="blog_subscription_email" />\n    <a href="#subscribe" ' \
                        'class="buttonize submit_form submit_subscribe">Subscribe</a>\n    </div>\n    <p class="notify">' \
                        'Don&rsquo;t worry; we hate spam with a passion.<br/>\n    You can unsubscribe with one click.</p>\n    ' \
                        '<span id="blog_extid">CKBUaGVd7rRdGWv3IJR</span>\n</form></section>\n<footer id="blog_foot" class="cf">\n ' \
                        ' <ul id="foot_links">\n    <li><a href="https://twitter.com/svbtle">@svbtle</a></li>\n    ' \
                        '<li><a href="mailto:hello@svbtle.com?subject=Svbtle">say hello</a></li>\n    ' \
                        '<li><a href="http://svbtle.com" >svbtle.com</a></li>\n  </ul>\n  <figure id="user_foot"><a href="/">Svbtle</a>' \
                        '</figure>\n  <h5><a href="//blog.svbtle.com">Svbtle Blog</a></h5>\n</footer>\n<div style="display: none;" ' \
                        'id="ssl_status">\nssl yes\n</div>\n<footer id="foot">\n  <figure id="logo_foot"><a href="https://svbtle.com">' \
                        'Svbtle</a></figure>\n  <a href="https://svbtle.com/terms" style="color: #ccc; margin-left: 25px;">Terms</a>' \
                        ' <span style="color: #ccc;">\xe2\x80\xa2</span> <a href="https://svbtle.com/privacy" style="color: #ccc;">' \
                        'Privacy</a> \n  <span style="color: #ccc;">\xe2\x80\xa2</span> <a href="https://svbtle.com/promise" ' \
                        'style="color: #ccc; margin-right: 15px;">Promise</a>\n  <br/><br/>\n</footer>\n<div id="lights">&nbsp;' \
                        '</div>\n<script>\n  var _sf_async_config = { uid: 1721, domain: \'svbtle.com\'};\n  (function() ' \
                        '{\n    function loadChartbeat() {\n      window._sf_endpt = (new Date()).getTime();\n      ' \
                        'var e = document.createElement(\'script\');\n      e.setAttribute(\'language\', \'javascript\');\n     ' \
                        ' e.setAttribute(\'type\', \'text/javascript\');\n      ' \
                        'e.setAttribute(\'src\',\'//static.chartbeat.com/js/chartbeat.js\');\n      document.body.appendChild(e);\n    };' \
                        '\n    var oldonload = window.onload;\n    window.onload = (typeof window.onload != \'function\') ?\n ' \
                        '     loadChartbeat : function() { oldonload(); loadChartbeat(); };\n  })();' \
                        '\n</script>\n</body>\n</html>\n'

FEED_DATA = '{"data":[{"id":"238936646561552_238942813227602","created_time":"2017-01-20T11:42:44+0000","picture":' \
            '"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-0\\/p130x130\\/16174951_238942813227602_6729719990182802617_n.jpg?' \
            'oh=bdf6b64184c84e586d445024d4a0690a&oe=593E9E58","updated_time":"2017-01-20T11:42:44+0000",' \
            '"story":"Test Page For Testing the APIs updated their profile picture.",' \
            '"link":"https:\\/\\/www.facebook.com\\/238936646561552\\/photos\\/a.238942809894269.1073741828.238936646561552\\' \
            '/238942813227602\\/?type=3","object_id":"238942813227602","attachments":' \
            '{"data":[{"media":{"image":{"height":169,"src":"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-9' \
            '\\/16174951_238942813227602_6729719990182802617_n.jpg?oh=c8d8eefe01a92a207a904556deb17e04&oe=594315D6","width":169}},' \
            '"target":{"id":"238936646561552","url":"https:\\/\\/www.facebook.com\\/Test-Page-For-Testing-the-APIs-238936646561552\\/"},' \
            '"title":"Test Page For Testing the APIs","type":"profile_media","url":"https:\\/\\/www.facebook.com\\/' \
            'Test-Page-For-Testing-the-APIs-238936646561552\\/"}]}},{"id":"238936646561552_238940673227816",' \
            '"created_time":"2017-01-20T11:39:46+0000","message":"Second  post with image","picture":"https:\\/\\/' \
            'scontent.xx.fbcdn.net\\/v\\/t1.0-0\\/s130x130\\/16003193_238940673227816_6582908959897565800_n.png?' \
            'oh=b562724894902cedcd18af00496c1cf5&oe=593D4A93","updated_time":"2017-01-20T11:39:46+0000",' \
            '"link":"https:\\/\\/www.facebook.com\\/238936646561552\\/photos\\/a.238939163227967.1073741827.238936646561552\\' \
            '/238940673227816\\/?type=3","object_id":"238940673227816","attachments":' \
            '{"data":[{"description":"Second  post with image","media":{"image":{"height":211,' \
            '"src":"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-9\\/16003193_238940673227816_6582908959897565800_n.png?' \
            'oh=4771a15ea15bec06a28d78f4a10fd4e1&oe=5939720E","width":570}},"target":{"id":"238940673227816","url":' \
            '"https:\\/\\/www.facebook.com\\/238936646561552\\/photos\\/a.238939163227967.1073741827.238936646561552\\' \
            '/238940673227816\\/?type=3"},"title":"Timeline Photos","type":"photo","url":"https:\\/\\/www.facebook.com\\' \
            '/238936646561552\\/photos\\/a.238939163227967.1073741827.238936646561552\\/238940673227816\\/?type=3"}]}},' \
            '{"id":"238936646561552_238939146561302","created_time":"2017-01-20T11:35:38+0000","message":"First Post With ' \
            'Images For testing","picture":"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-0\\/s130x130\\' \
            '/16174713_238939146561302_1711728766524725562_n.jpg?oh=f6ddd00aacfd4dd3ddd465b0d126304a&oe=594B8C97",' \
            '"updated_time":"2017-01-20T11:35:38+0000","link":"https:\\/\\/www.facebook.com\\/238936646561552\\/photos\\/' \
            'a.238939163227967.1073741827.238936646561552\\/238939146561302\\/?type=3","object_id":"238939146561302",' \
            '"attachments":{"data":[{"description":"First Post With Images For testing","media":{"image":' \
            '{"height":169,"src":"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-9\\/16174713_238939146561302_1711728766524725562_n.jpg?' \
            'oh=e49010f242bf33af69d7bc0160776235&oe=5937F20A","width":225}},"target":{"id":"238939146561302","url":' \
            '"https:\\/\\/www.facebook.com\\/238936646561552\\/photos\\/a.238939163227967.1073741827.238936646561552\\' \
            '/238939146561302\\/?type=3"},"title":"Timeline Photos","type":"photo","url":"https:\\/\\/www.facebook.com\\' \
            '/238936646561552\\/photos\\/a.238939163227967.1073741827.238936646561552\\/238939146561302\\/?type=3"}]}},' \
            '{"id":"238936646561552_238939013227982","created_time":"2017-01-20T11:35:08+0000","picture":"https:\\/\\/' \
            'scontent.xx.fbcdn.net\\/v\\/t1.0-0\\/s130x130\\/16143352_238939013227982_3816944016185173076_n.jpg?oh=' \
            'dc8c55ae9265bc7f00c83464f9cf5837&oe=592D5459","updated_time":"2017-01-20T11:35:08+0000","story":' \
            '"Test Page For Testing the APIs updated their cover photo.","link":"https:\\/\\/www.facebook.com\\/238936646561552\\' \
            '/photos\\/a.238939053227978.1073741826.238936646561552\\/238939013227982\\/?type=3","object_id":"238939013227982",' \
            '"attachments":{"data":[{"media":{"image":{"height":507,"src":"https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t1.0-9\\/s720x720\\' \
            '/16143352_238939013227982_3816944016185173076_n.jpg?oh=bcd09b917c51f99c867d5b3fdfdee6fd&oe=5903B3A6","width":720}},' \
            '"target":{"id":"238936646561552","url":"https:\\/\\/www.facebook.com\\/Test-Page-For-Testing-the-APIs-238936646561552\\/"},' \
            '"title":"Test Page For Testing the APIs\'s cover photo","type":"cover_photo","url":"https:\\/\\/www.facebook.com\\/' \
            'Test-Page-For-Testing-the-APIs-238936646561552\\/"}]}},{"id":"238936646561552_238938306561386",' \
            '"created_time":"2017-01-20T11:31:39+0000","message":"Second post with images for page creation","updated_time":"2017-01-20T11:31:39+0000"},' \
            '{"id":"238936646561552_238938079894742","created_time":"2017-01-20T11:30:57+0000","message":"This is first post for the app creation",' \
            '"updated_time":"2017-01-20T11:30:57+0000"}],"paging":{"previous":"https:\\/\\/graph.facebook.com\\/v2.8\\/238936646561552\\' \
            '/feed?fields=id,description,created_time,message,picture,updated_time,attachments,story,properties,link,' \
            'object_id&since=1484912564&access_token=EAADk4jRYN0sBAAZC0pMd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4' \
            'DtCI6ZCtE0latZByOTkreFUlKoGOJoSdu3SdqEHZCkYKhUSuV0aKt4enlKHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqK' \
            'yEL7V0SwZDZD&limit=25&__paging_token=enc_AdC6DMIU2m8LKX6PoOMwPnZAXnlL8e9DUYZAZCBj41WlWes9GbdRinDZCdkuUooO39mshuq' \
            'PVuNBelk0bINO0ZBuFYCPFFJl9QHn3ICvVFK7e7AtYIwZDZD&__previous=1",' \
            '"next":"https:\\/\\/graph.facebook.com\\/v2.8\\/238936646561552\\/feed?fields=id,' \
            'description,created_time,message,picture,updated_time,attachments,story,properties,link,object_id' \
            '&access_token=EAADk4jRYN0sBAAZC0pMd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4DtCI6ZCtE0latZByOTkreFUlKo' \
            'GOJoSdu3SdqEHZCkYKhUSuV0aKt4enlKHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqKyEL7V0SwZDZD&limit=25&until=' \
            '1484911857&__paging_token=enc_AdClKuTmEpBkgwd4eZCZB7L4Jov48N4DMwjH1ENPfuH2kD7l4BMrELUVnsq05eweftLOWGH39E3TFYW' \
            '31wI96vaomSav31bQCo8B1bZAmLP1Kw55QZDZD"}}'


FACEBOOK_PAGE_FEEDS_DATA = {
    'data': [{
        'link': 'https://www.facebook.com/238936646561552/photos/a.238942809894269.1073741828.238936646561552/'
                '238942813227602/?type=3',
        'object_id': '238942813227602',
        'id': '238936646561552_238942813227602',
        'updated_time': '2017-01-20T11:42:44+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/p130x130/16174951_238942813227602_6729719990182802617_'
                   'n.jpg?oh=bdf6b64184c84e586d445024d4a0690a&oe=593E9E58',
        'attachments': {
            'data': [{
                'title': 'Test Page For Testing the APIs',
                'type': 'profile_media',
                'target': {
                    'id': '238936646561552',
                    'url': 'https://www.facebook.com/Test-Page-For-Testing-the-APIs-238936646561552/'
                },
                'media': {
                    'image': {
                        'height': 169,
                        'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/16174951_238942813227602_6729719990182'
                               '802617_n.jpg?oh=c8d8eefe01a92a207a904556deb17e04&oe=594315D6',
                        'width': 169
                    }
                },
                'url': 'https://www.facebook.com/Test-Page-For-Testing-the-APIs-238936646561552/'
            }]
        },
        'created_time': '2017-01-20T11:42:44+0000',
        'story': 'Test Page For Testing the APIs updated their profile picture.'
    }, {
        'link': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.238936646561'
                '552/238940673227816/?type=3',
        'object_id': '238940673227816',
        'id': '238936646561552_238940673227816',
        'updated_time': '2017-01-20T11:39:46+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/s130x130/16003193_238940673227816_658290895'
                   '9897565800_n.png?oh=b562724894902cedcd18af00496c1cf5&oe=593D4A93',
        'attachments': {
            'data': [{
                'title': 'Timeline Photos',
                'media': {
                    'image': {
                        'height': 211,
                        'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/16003193_238940673227816_6582908959897565800_'
                               'n.png?oh=4771a15ea15bec06a28d78f4a10fd4e1&oe=5939720E',
                        'width': 570
                    }
                },
                'description': 'Second  post with image',
                'url': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.238936646561552/2'
                       '38940673227816/?type=3',
                'type': 'photo',
                'target': {
                    'id': '238940673227816',
                    'url': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.2389366465'
                           '61552/238940673227816/?type=3'
                }
            }]
        },
        'created_time': '2017-01-20T11:39:46+0000',
        'message': 'Second  post with image'
    }, {
        'link': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.238936646561552/2389'
                '39146561302/?type=3',
        'object_id': '238939146561302',
        'id': '238936646561552_238939146561302',
        'updated_time': '2017-01-20T11:35:38+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/s130x130/16174713_238939146561302_171172876652472'
                   '5562_n.jpg?oh=f6ddd00aacfd4dd3ddd465b0d126304a&oe=594B8C97',
        'attachments': {
            'data': [{
                'title': 'Timeline Photos',
                'media': {
                    'image': {
                        'height': 169,
                        'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/16174713_238939146561302_171172876652472'
                               '5562_n.jpg?oh=e49010f242bf33af69d7bc0160776235&oe=5937F20A',
                        'width': 225
                    }
                },
                'description': 'First Post With Images For testing',
                'url': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.238936646'
                       '561552/238939146561302/?type=3',
                'type': 'photo',
                'target': {
                    'id': '238939146561302',
                    'url': 'https://www.facebook.com/238936646561552/photos/a.238939163227967.1073741827.238936'
                           '646561552/238939146561302/?type=3'
                }
            }]
        },
        'created_time': '2017-01-20T11:35:38+0000',
        'message': 'First Post With Images For testing'
    }, {
        'link': 'https://www.facebook.com/238936646561552/photos/a.238939053227978.1073741826.238936646561552/23893'
                '9013227982/?type=3',
        'object_id': '238939013227982',
        'id': '238936646561552_238939013227982',
        'updated_time': '2017-01-20T11:35:08+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/s130x130/16143352_238939013227982_3816944016185173076_n.jp'
                   'g?oh=dc8c55ae9265bc7f00c83464f9cf5837&oe=592D5459',
        'attachments': {
            'data': [{
                'title': "Test Page For Testing the APIs's cover photo",
                'type': 'cover_photo',
                'target': {
                    'id': '238936646561552',
                    'url': 'https://www.facebook.com/Test-Page-For-Testing-the-APIs-238936646561552/'
                },
                'media': {
                    'image': {
                        'height': 507,
                        'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/16143352_238939013227982_3816944016'
                               '185173076_n.jpg?oh=bcd09b917c51f99c867d5b3fdfdee6fd&oe=5903B3A6',
                        'width': 720
                    }
                },
                'url': 'https://www.facebook.com/Test-Page-For-Testing-the-APIs-238936646561552/'
            }]
        },
        'created_time': '2017-01-20T11:35:08+0000',
        'story': 'Test Page For Testing the APIs updated their cover photo.'
    }, {
        'id': '238936646561552_238938306561386',
        'updated_time': '2017-01-20T11:31:39+0000',
        'created_time': '2017-01-20T11:31:39+0000',
        'message': 'Second post with images for page creation'
    }, {
        'id': '238936646561552_238938079894742',
        'updated_time': '2017-01-20T11:30:57+0000',
        'created_time': '2017-01-20T11:30:57+0000',
        'message': 'This is first post for the app creation'
    }],
    'paging': {
        'previous': 'https://graph.facebook.com/v2.8/238936646561552/feed?fields=id,description,created_time,message'
                    ',picture,updated_time,attachments,story,properties,link,object_id&since=1484912564&access_token='
                    'EAADk4jRYN0sBAAZC0pMd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4DtCI6ZCtE0latZByOTkreFUlKoGO'
                    'JoSdu3Sdq'
                    'EHZCkYKhUSuV0aKt4enlKHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqKyEL7V0SwZDZD&limit=25&'
                    '__paging_toke'
                    'n=enc_AdC6DMIU2m8LKX6PoOMwPnZAXnlL8e9DUYZAZCBj41WlWes9GbdRinDZCdkuUooO39mshuqPVuNBelk0bI'
                    'NO0ZBuFYCPFF'
                    'Jl9QHn3ICvVFK7e7AtYIwZDZD&__previous=1',
        'next': 'https://graph.facebook.com/v2.8/238936646561552/feed?fields=id,description,created_time,message,'
                'picture,updated_time,attachments,story,properties,link,object_id&access_token=EAADk4jRYN0sBAAZC0pM'
                'd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4DtCI6ZCtE0latZByOTkreFUlKoGOJoSdu3SdqEHZCkYKhUSuV0aKt4e'
                'nlKHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqKyEL7V0SwZDZD&limit=25&until=1484911857&__pagin'
                'g_token=enc_AdClKuTmEpBkgwd4eZCZB7L4Jov48N4DMwjH1ENPfuH2kD7l4BMrELUVnsq05eweftLOWGH39E3TFYW31wI9'
                '6vaomSav31bQCo8B1bZAmLP1Kw55QZDZD'
    }
}

FACEBOOK_USER_FEEDS_DATA = {
    'data': [{
        'story': 'Ram Chauhan added 2 new photos.',
        'link': 'https://www.facebook.com/photo.php?fbid=146589425849309&set=a.117168022124783.1073741826.100014'
                '947571964&type=3',
        'object_id': '146589425849309',
        'id': '117076328800619_146589772515941',
        'updated_time': '2017-02-07T09:31:54+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/s130x130/16602650_146589425849309_6183762155372834499'
                   '_n.jpg?oh=7346cff1b22c6353e029a431e24f78d0&oe=593D5E68',
        'attachments': {
            'data': [{
                'title': "Photos from Ram Chauhan's post",
                'type': 'album',
                'subattachments': {
                    'data': [{
                        'type': 'photo',
                        'target': {
                            'id': '146589425849309',
                            'url': 'https://www.facebook.com/photo.php?fbid=146589425849309&set=p.1465894258'
                                   '49309&type=3'
                        },
                        'media': {
                            'image': {
                                'height': 169,
                                'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/16602650_146589425849309_6'
                                       '183762155372834499_n.jpg?oh=bf5f952162d9560fd3b1f20c4c94e01f&oe=5941ADF5',
                                'width': 225
                            }
                        },
                        'url': 'https://www.facebook.com/photo.php?fbid=146589425849309&set=p.14658942'
                               '5849309&type=3'
                    }, {
                        'type': 'photo',
                        'target': {
                            'id': '146589432515975',
                            'url': 'https://www.facebook.com/photo.php?fbid=146589432515975&set=p.1465894'
                                   '32515975&type=3'
                        },
                        'media': {
                            'image': {
                                'height': 211,
                                'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/16473592_146589432515975_5668'
                                       '857021542601908_n.jpg?oh=faf9e3828684c2867645e450f8e0c248&oe=58FFF516',
                                'width': 570
                            }
                        },
                        'url': 'https://www.facebook.com/photo.php?fbid=146589432515975&set=p.14658943251'
                               '5975&type=3'
                    }]
                },
                'target': {
                    'id': '146589772515941',
                    'url': 'https://www.facebook.com/permalink.php?story_fbid=146589772515941&id=100014947571964'
                },
                'url': 'https://www.facebook.com/permalink.php?story_fbid=146589772515941&id=100014947571964'
            }]
        },
        'created_time': '2017-02-07T09:31:54+0000',
        'message': 'dskjfds\nfgds\ngdsag\n\ndsg\nds\ng\ndfg\ndsg\ndf\ngdfgdfsgdfsgdfsgdfsgdfsgdfstete5rt54t545465'
                   '4654t546546546546546546546546546867867'
    }, {
        'link': 'https://www.facebook.com/photo.php?fbid=117167955458123&set=a.117168022124783.1073741826.10001494'
                '7571964&type=3',
        'object_id': '117167955458123',
        'id': '117076328800619_117168025458116',
        'updated_time': '2017-01-17T07:42:33+0000',
        'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-0/s130x130/15977857_117167955458123_1642149347986992311_n.'
                   'jpg?oh=1a56ae2f8f614f7e326d1a3f758678a9&oe=594540E8',
        'attachments': {
            'data': [{
                'type': 'photo',
                'target': {
                    'id': '117167955458123',
                    'url': 'https://www.facebook.com/photo.php?fbid=117167955458123&set=p.117167955458123&type=3'
                },
                'media': {
                    'image': {
                        'height': 479,
                        'src': 'https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/15977857_117167955458123_164214934798'
                               '6992311_n.jpg?oh=bd6111f688f932210ade60128dc9657a&oe=593CEA17',
                        'width': 720
                    }
                },
                'description': 'second post with images',
                'url': 'https://www.facebook.com/photo.php?fbid=117167955458123&set=p.117167955458123&type=3'
            }]
        },
        'created_time': '2017-01-17T07:42:33+0000',
        'message': 'second post with images'
    }, {
        'id': '117076328800619_117148285460090',
        'updated_time': '2017-01-17T07:24:49+0000',
        'created_time': '2017-01-17T07:24:49+0000',
        'message': 'First post with no image'
    }],
    'paging': {
        'previous': 'https://graph.facebook.com/v2.8/117076328800619/feed?fields=id,description,created_time,mess'
                    'age,picture,updated_time,attachments,story,properties,link,object_id&since=1486459914&acces'
                    's_token=EAADk4jRYN0sBAAZC0pMd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4DtCI6ZCtE0latZByOTkre'
                    'FUlKoGOJoSdu3SdqEHZCkYKhUSuV0aKt4enlKHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqKyEL7V0Sw'
                    'ZDZD&limit=25&__paging_token=enc_AdB5t09ZBL2b3L1MzR6HQNgC8MZBGusMjmM1AkeAC2obZCra5saJQDjytx'
                    '2QJeZAOTZBckmnkw62WcDxgjqeyM0YlD4kCOsNqVIIm4SEkcyvrAzG31QZDZD&__previous=1',
        'next': 'https://graph.facebook.com/v2.8/117076328800619/feed?fields=id,description,created_time,messag'
                'e,picture,updated_time,attachments,story,properties,link,object_id&access_token=EAADk4jRYN0sBAAZC0pM'
                'd4HRZAsb0YMYN7kfkq1qPjxKvxprHau1zFI3xV1jA4DtCI6ZCtE0latZByOTkreFUlKoGOJoSdu3SdqEHZCkYKhUSuV0aKt4enl'
                'KHfHlaYYPO83qFLHjtnByzYCtHwvQvYAxwEr2ZAY6LTlqKyEL7V0SwZDZD&limit=25&until=1484637889&__paging_to'
                'ken=enc_AdC7Y3H5Mx41VRZBlzzsnJ3MMrLHWZCLQhLXCWUz3ESUCXvImbkFjsmyZC1bZAEQRveCJwYbNA3Nc7KQLDSSTrr'
                'dzaendoWpKBiYMAcb4NptyxBWnAZDZD'
    }
}

INSTAGRAM_USER_FEEDS_DATA = {
    'pagination': {},
    'data': [{
        'user': {
            'full_name': 'Atlogys',
            'id': '4468395084',
            'username': 'atlogys1652',
            'profile_picture': 'https://scontent-otp1-1.cdninstagram.com/t51.2885-19/11906329_960233084022564_1448'
                               '528159_a.jpg'
        },
        'images': {
            'standard_resolution': {
                'height': 294,
                'width': 320,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/e35/16111011_1574809185862888_38840041706'
                       '20993536_n.jpg?ig_cache_key=MTQzMDQ1NjU0NTQ1NTU5MzU1NA%3D%3D.2'
            },
            'low_resolution': {
                'height': 294,
                'width': 320,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/e35/16111011_1574809185862888_3884004170620'
                       '993536_n.jpg?ig_cache_key=MTQzMDQ1NjU0NTQ1NTU5MzU1NA%3D%3D.2'
            },
            'thumbnail': {
                'height': 150,
                'width': 150,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/c13.0.294.294/16111011_1574809185862'
                       '888_3884004170620993536_n.jpg?ig_cache_key=MTQzMDQ1NjU0NTQ1NTU5MzU1NA%3D%3D.2.c'
            }
        },
        'link': 'https://www.instagram.com/p/BPaAKYyg1hS/',
        'likes': {
            'count': 1
        },
        'user_has_liked': True,
        'comments': {
            'count': 0
        },
        'created_time': '1484743730',
        'tags': [],
        'filter': 'Normal',
        'caption': None,
        'id': '1430456545455593554_4468395084',
        'location': None,
        'users_in_photo': [],
        'type': 'image',
        'attribution': None
    }, {
        'user': {
            'full_name': 'Atlogys',
            'id': '4468395084',
            'username': 'atlogys1652',
            'profile_picture': 'https://scontent-otp1-1.cdninstagram.com/t51.2885-19/11906329_960233084022564_14'
                               '48528159_a.jpg'
        },
        'images': {
            'standard_resolution': {
                'height': 640,
                'width': 640,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/15623809_105420074468'
                       '5298_5545303082696441856_n.jpg?ig_cache_key=MTQzMDQ1NjQ0MTg5ODEwNTExNQ%3D%3D.2'
            },
            'low_resolution': {
                'height': 320,
                'width': 320,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/15623809_1054200744685298_5'
                       '545303082696441856_n.jpg?ig_cache_key=MTQzMDQ1NjQ0MTg5ODEwNTExNQ%3D%3D.2'
            },
            'thumbnail': {
                'height': 150,
                'width': 150,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/15623809_1054200744685298_55453'
                       '03082696441856_n.jpg?ig_cache_key=MTQzMDQ1NjQ0MTg5ODEwNTExNQ%3D%3D.2'
            }
        },
        'link': 'https://www.instagram.com/p/BPaAI4WAXkb/',
        'likes': {
            'count': 0
        },
        'user_has_liked': False,
        'comments': {
            'count': 0
        },
        'created_time': '1484743717',
        'tags': [],
        'filter': 'Normal',
        'caption': None,
        'id': '1430456441898105115_4468395084',
        'location': None,
        'users_in_photo': [],
        'type': 'image',
        'attribution': None
    }, {
        'user': {
            'full_name': 'Atlogys',
            'id': '4468395084',
            'username': 'atlogys1652',
            'profile_picture': 'https://scontent-otp1-1.cdninstagram.com/t51.2885-19/11906329_960233084022564_14'
                               '48528159_a.jpg'
        },
        'images': {
            'standard_resolution': {
                'height': 640,
                'width': 640,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/16124013_1322069167849'
                       '944_2370359014342000640_n.jpg'
            },
            'low_resolution': {
                'height': 320,
                'width': 320,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/16124013_1322069167849944_237035'
                       '9014342000640_n.jpg'
            },
            'thumbnail': {
                'height': 150,
                'width': 150,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/16124013_1322069167849944_2370359'
                       '014342000640_n.jpg'
            }
        },
        'link': 'https://www.instagram.com/p/BPaAFFVgFuV/',
        'likes': {
            'count': 0
        },
        'user_has_liked': False,
        'comments': {
            'count': 0
        },
        'created_time': '1484743686',
        'tags': [],
        'filter': 'Normal',
        'caption': None,
        'id': '1430456180970380181_4468395084',
        'location': None,
        'users_in_photo': [],
        'type': 'image',
        'attribution': None
    }, {
        'user': {
            'full_name': 'Atlogys',
            'id': '4468395084',
            'username': 'atlogys1652',
            'profile_picture': 'https://scontent-otp1-1.cdninstagram.com/t51.2885-19/11906329_960233084022564_14485'
                               '28159_a.jpg'
        },
        'images': {
            'standard_resolution': {
                'height': 640,
                'width': 640,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/16123668_103667371314474'
                       '1_6339932978042372096_n.jpg'
            },
            'low_resolution': {
                'height': 320,
                'width': 320,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/16123668_1036673713144741_63399'
                       '32978042372096_n.jpg'
            },
            'thumbnail': {
                'height': 150,
                'width': 150,
                'url': 'https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/16123668_1036673713144741_633993'
                       '2978042372096_n.jpg'
            }
        },
        'link': 'https://www.instagram.com/p/BPaAAsRg4j1/',
        'likes': {
            'count': 0
        },
        'user_has_liked': False,
        'comments': {
            'count': 0
        },
        'created_time': '1484743650',
        'tags': [],
        'filter': 'Normal',
        'caption': None,
        'id': '1430455879182026997_4468395084',
        'location': None,
        'users_in_photo': [],
        'type': 'image',
        'attribution': None
    }],
    'meta': {
        'code': 200
    }
}


YOUTUBE_CHANEL_FEEDS_DATA = {
    'pageInfo': {
        'resultsPerPage': 50,
        'totalResults': 3
    },
    'regionCode': 'IN',
    'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/4HIFIM6xbgE0KXDXbNguWdAwt7g"',
    'items': [{
        'snippet': {
            'publishedAt': '2017-01-19T10:17:13.000Z',
            'channelId': 'UCPfWeVkvkmm_UMEUCQ6-hVg',
            'title': 'Ram Chauhan',
            'liveBroadcastContent': 'none',
            'description': 'This is for testing the API call with the google APIs.',
            'thumbnails': {
                'high': {
                    'url': 'https://yt3.ggpht.com/-1ddE9aUXgZM/AAAAAAAAAAI/AAAAAAAAAAA/mCuHAgvSJtg/s240-c-k-no-mo-'
                           'rj-c0xffffff/photo.jpg'
                },
                'medium': {
                    'url': 'https://yt3.ggpht.com/-1ddE9aUXgZM/AAAAAAAAAAI/AAAAAAAAAAA/mCuHAgvSJtg/s240-c-k-no-mo-'
                           'rj-c0xffffff/photo.jpg'
                },
                'default': {
                    'url': 'https://yt3.ggpht.com/-1ddE9aUXgZM/AAAAAAAAAAI/AAAAAAAAAAA/mCuHAgvSJtg/s88-c-k-no-mo-'
                           'rj-c0xffffff/photo.jpg'
                }
            },
            'channelTitle': 'Ram Chauhan'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/6KbK1s-8IT1PlPHiwgq1oATcuT4"',
        'id': {
            'channelId': 'UCPfWeVkvkmm_UMEUCQ6-hVg',
            'kind': 'youtube#channel'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-19T10:40:19.000Z',
            'channelId': 'UCPfWeVkvkmm_UMEUCQ6-hVg',
            'title': 'Monkey Playing With Child',
            'liveBroadcastContent': 'none',
            'description': 'Test Video For Application Processing.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/mG7ogCRnmF0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/mG7ogCRnmF0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/mG7ogCRnmF0/default.jpg'
                }
            },
            'channelTitle': 'Ram Chauhan'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/lwmhz9bWG5HenQxEGzyrATc0ut0"',
        'id': {
            'videoId': 'mG7ogCRnmF0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-19T10:58:30.000Z',
            'channelId': 'UCPfWeVkvkmm_UMEUCQ6-hVg',
            'title': 'Second Video Upload for Feed app',
            'liveBroadcastContent': 'none',
            'description': 'This video is uploaded for testing the google API for feed.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/CkfKTUe_sAY/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/CkfKTUe_sAY/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/CkfKTUe_sAY/default.jpg'
                }
            },
            'channelTitle': 'Ram Chauhan'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/hptbC-FzB9GwYSduawwfFRc1u8k"',
        'id': {
            'videoId': 'CkfKTUe_sAY',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }],
    'kind': 'youtube#searchListResponse'
}


YOUTUBE_USER_FEEDS_DATA = {
    'nextPageToken': 'CDIQAA',
    'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/e7W3dDZUte_utcFKb8byHRKmK0E"',
    'pageInfo': {
        'resultsPerPage': 50,
        'totalResults': 1000000
    },
    'regionCode': 'IN',
    'items': [{
        'snippet': {
            'publishedAt': '2014-12-15T16:49:39.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Steven Spielberg vs Alfred Hitchcock.   Epic Rap Battles of History.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song here ▻ http://hyperurl.co/The-Directors ◅ Watch the Behind '
                           'The Scenes here: http://bit.ly/136ILCt "Rap Battles are life with all the dull'
                           ' bits ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/_wYtG7aQTHA/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/_wYtG7aQTHA/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/_wYtG7aQTHA/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/wI1kuyQA0AeTEje1ieUUVFQ899w"',
        'id': {
            'videoId': '_wYtG7aQTHA',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-06-14T07:01:29.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Steve Jobs vs Bill Gates.  Epic Rap Battles of History Season 2.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Jobs-vs-Gates ◅ Watch behind the '
                           'scenes ▻ http://bit.ly/jobgates ◅ Check out our NEW Trump vs Clinton T-shirts ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/njos57IJf-0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/njos57IJf-0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/njos57IJf-0/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/CLyaY-TFpQ3pBNLiDo_fqg9LKSg"',
        'id': {
            'videoId': 'njos57IJf-0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-06-16T17:02:33.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Sir Isaac Newton vs Bill Nye. Epic Rap Battles of History Season 3.',
            'liveBroadcastContent': 'none',
            'description': 'Download This Song: ▻ http://hyperurl.co/Newton-vs-Nye ◅ Watch behind the scenes ▻ '
                           'http://bit.ly/newtonnye ◅ "If I have seen further than others, it is by ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/8yis7GzlXNM/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/8yis7GzlXNM/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/8yis7GzlXNM/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/Q2NpmfRJ2K627PwjyvsEfmUfpW8"',
        'id': {
            'videoId': '8yis7GzlXNM',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-02-21T14:00:00.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': 'Taylor Swift and Zac Efron Sing a Duet!',
            'liveBroadcastContent': 'none',
            'description': "This incredible duo teamed up to perform an original song for Ellen! They may not "
                           "have had a lot of rehearsal, but it's clear that this is one musical combo it ...",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/d8kCTPPwfpM/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/d8kCTPPwfpM/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/d8kCTPPwfpM/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/hsQmFEqp1R_glFpcQnpnOLbbxCg"',
        'id': {
            'videoId': 'd8kCTPPwfpM',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-07-20T23:42:54.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Shaka Zulu vs Julius Caesar.  Epic Rap Battles of History Season 4.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Zulu-vs-Caesar ◅ Watch Behind The Scenes '
                           '▻http://bit.ly/ZuluBTS◅ "It is better to create than to learn! Creating is the ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/oOm_2dGzqp0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/oOm_2dGzqp0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/oOm_2dGzqp0/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/YzcsKitG_GeT5oumFsvlpnQ6OAY"',
        'id': {
            'videoId': 'oOm_2dGzqp0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2013-10-21T13:00:06.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Blackbeard vs Al Capone.  Epic Rap Battles of History Season 3.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song: ▻ http://hyperurl.co/Blackbeard-vs-Capone ◅ Watch the behind '
                           'the scenes: ▻ http://bit.ly/blackcapone ◅ "The rougher the seas, the ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/yf9gulYfUh4/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/yf9gulYfUh4/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/yf9gulYfUh4/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/b4p7lCMS190UjIv7NQy-ormFFec"',
        'id': {
            'videoId': 'yf9gulYfUh4',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-12-01T14:15:00.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Jack the Ripper vs Hannibal Lecter.  Epic Rap Battles of History Season 4.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Ripper-vs-Lecter ◅ Watch Behind The Scenes'
                           ' Here: ▻ http://bit.ly/12jUUnc◅ "I do wish we could battle longer, but I\'m ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/KfkR5o_bcSg/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/KfkR5o_bcSg/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/KfkR5o_bcSg/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/yi_BeUpr_qnIbMC6HZOOjq6be0g"',
        'id': {
            'videoId': 'KfkR5o_bcSg',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-07-14T13:00:07.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Artists vs TMNT. Epic Rap Battles of History Season 3 Finale.',
            'liveBroadcastContent': 'none',
            'description': 'Download This Song: ▻ http://hyperurl.co/Artists-vs-Turtles ◅ Watch behind the'
                           ' scenes ▻ http://bit.ly/TMNTart ◅ "Who\'s ready for a pizza Season 5.5 action?',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/6HZ5V9rT96M/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/6HZ5V9rT96M/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/6HZ5V9rT96M/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/Afl3L54lUSdAdaEv80DBmeHVp6M"',
        'id': {
            'videoId': '6HZ5V9rT96M',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-07-06T22:37:02.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Eastern Philosophers vs Western Philosophers.  Epic Rap Battles of History Season 4.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Philosophers-EvsW ◅ Watch Behind The Scenes'
                           ' ▻http://bit.ly/Philosophers-BTS ◅ "It does not matter how slowly you ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/0N_RO-jL-90/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/0N_RO-jL-90/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/0N_RO-jL-90/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/HXnm7oemvnqC43yPEQx00Ykl4tM"',
        'id': {
            'videoId': '0N_RO-jL-90',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-05-03T03:33:02.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'J. R. R. Tolkien vs George R. R. Martin.  Epic Rap Battles of History. Season 5',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Tolkien-vs-Martin ◅ Watch the Behind the '
                           'Scenes ▻http://bit.ly/ERB_BTS◅ Listen and follow on Spotify ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/XAAp_luluo0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/XAAp_luluo0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/XAAp_luluo0/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/wrsi_7tX7u44-4AYKCz0Tt25pig"',
        'id': {
            'videoId': 'XAAp_luluo0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-05-05T13:00:06.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Rick Grimes vs Walter White.  Epic Rap Battles of History Season 3.',
            'liveBroadcastContent': 'none',
            'description': 'Download This Song: ▻ http://hyperurl.co/Grimes-vs-White ◅ Watch behind the scenes'
                           ' ▻ http://bit.ly/grimewhite ◅ "Just because you shot Rick Grimes, doesn\'t ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/krQHQvtIr6w/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/krQHQvtIr6w/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/krQHQvtIr6w/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/7qVI4NgVpLE28tDkul7PArMorW8"',
        'id': {
            'videoId': 'krQHQvtIr6w',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-06-02T13:00:07.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Stephen King vs Edgar Allan Poe. Epic Rap Battles of History Season 3.',
            'liveBroadcastContent': 'none',
            'description': 'Download This Song: ▻ http://hyperurl.co/King-vs-Poe ◅ Watch behind the scenes '
                           '▻ http://bit.ly/kingpoe ◅ "Monsters are real, and ghosts are real too.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/56R3hU-fWZY/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/56R3hU-fWZY/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/56R3hU-fWZY/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/9cB6XgVwvp3Mk6QvmSDwzy8I8y8"',
        'id': {
            'videoId': '56R3hU-fWZY',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-04-02T21:48:54.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Michael Jackson VS Elvis Presley.  Epic Rap Battles of History Season 2.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Jackson-vs-Presley ◅ Watch behind the scenes'
                           ' ▻ http://bit.ly/jackelvis ◅ "The Kings are dead, long live the kings" ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/0M0RbaPxq2k/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/0M0RbaPxq2k/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/0M0RbaPxq2k/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/GhFMMd_Ma9tYeHF0B1PtTyYVWts"',
        'id': {
            'videoId': '0M0RbaPxq2k',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-12-26T22:33:33.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Theodore Roosevelt vs Winston Churchill. Epic Rap Battles of History',
            'liveBroadcastContent': 'none',
            'description': 'New ERB Swag is in! http://ERBMerch.com Download this song: http://hyperurl.co'
                           '/TeddyVsWinston Watch the Behind the Scenes ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/owTPZQQAVyQ/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/owTPZQQAVyQ/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/owTPZQQAVyQ/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/zc_mgbnCWPv1rjKLygf8BVGuJg4"',
        'id': {
            'videoId': 'owTPZQQAVyQ',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-02-17T00:46:04.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Mario Bros vs Wright Bros.  Epic Rap Battles of History Season 2',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Mario-vs-Wright ◅ Watch behind the scenes'
                           ' ▻ http://bit.ly/mariowright ◅ "Nighty nighty. Ah spaghetti. Ah, ravioli. Ahh ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/1_hKLfTKU5Y/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/1_hKLfTKU5Y/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/1_hKLfTKU5Y/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/qBa0TeOq_VolMVvJ7sMa3hkz9dQ"',
        'id': {
            'videoId': '1_hKLfTKU5Y',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-01-06T04:49:00.000Z',
            'channelId': 'UCi7GJNg51C3jgmYTUwqoUXA',
            'title': 'Ice Cube, Kevin Hart And Conan Help A Student Driver  - CONAN on TBS',
            'liveBroadcastContent': 'none',
            'description': 'CONAN Highlight: A CONAN staffer is learning the rules of the road, with a little '
                           'help from Kevin Hart, Ice Cube, & Conan. Look out, fellow drivers! More CONAN ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/1Za8BtLgKv8/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/1Za8BtLgKv8/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/1Za8BtLgKv8/default.jpg'
                }
            },
            'channelTitle': 'Team Coco'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/kgwvHkfyrLwgDQSoGh8jH_qbax0"',
        'id': {
            'videoId': '1Za8BtLgKv8',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-03-29T19:03:13.000Z',
            'channelId': 'UCi7GJNg51C3jgmYTUwqoUXA',
            'title': 'Disturbed "The Sound Of Silence" 03/28/16',
            'liveBroadcastContent': 'none',
            'description': 'Disturbed performs a track from their album Immortalized. More CONAN @ http://teamcoco.'
                           'com/video Team Coco is the official YouTube channel of late night ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/Bk7RVw3I8eg/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/Bk7RVw3I8eg/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/Bk7RVw3I8eg/default.jpg'
                }
            },
            'channelTitle': 'Team Coco'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/EtQ8_na6Ex5Q1J_ThFf_E7x7LSE"',
        'id': {
            'videoId': 'Bk7RVw3I8eg',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-10-31T16:07:49.000Z',
            'channelId': 'UCC552Sd-3nyi_tk2BudLUzA',
            'title': 'The NEW Periodic Table Song (Updated)',
            'liveBroadcastContent': 'none',
            'description': 'Download on ITUNES: http://bit.ly/12AeW99 Hey friends - we wanted to update a few '
                           'things in our video to be more accurate and appropriate for everyone.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/VgVQKCcfwnU/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/VgVQKCcfwnU/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/VgVQKCcfwnU/default.jpg'
                }
            },
            'channelTitle': 'AsapSCIENCE'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/JngNnN6xc-zZlO2Mb9-EC-PTDT4"',
        'id': {
            'videoId': 'VgVQKCcfwnU',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-02-18T14:00:00.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': "Adele Performs\xa0'All\xa0I\xa0Ask'",
            'liveBroadcastContent': 'none',
            'description': 'The amazing Adele belted out her hit song for the first time since her Grammy '
                           'performance.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/4aKteL3vMvU/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/4aKteL3vMvU/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/4aKteL3vMvU/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/M9siwkGRaHrf5ELg2R1JceH2KmA"',
        'id': {
            'videoId': '4aKteL3vMvU',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2013-04-23T03:56:43.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Rasputin vs Stalin.  Epic Rap Battles of History Season 2 finale.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Rasputin-vs-Stalin ◅ Watch behind the '
                           'scenes ▻ http://bit.ly/stalinrasp ◅ "There are no short cuts to any place worth ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/ZT2z0nrsQ8o/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/ZT2z0nrsQ8o/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/ZT2z0nrsQ8o/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/jpEZSgf6JTRQrPpk2L-jWLi6khA"',
        'id': {
            'videoId': 'ZT2z0nrsQ8o',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2013-04-08T16:00:48.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Mozart vs Skrillex. Epic Rap Battles of History Season 2.',
            'liveBroadcastContent': 'none',
            'description': 'Download This Song: ▻ http://hyperurl.co/Mozart-vs-Skrillex ◅ Watch behind the '
                           'scenes ▻ http://bit.ly/mozartskrill ◅ "Season 5.5 is upon us. Thank you for your ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/_6Au0xCg3PI/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/_6Au0xCg3PI/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/_6Au0xCg3PI/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/nkgbyWmAdhsE1PWhzzn3WAy3YKE"',
        'id': {
            'videoId': '_6Au0xCg3PI',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-10-15T17:01:09.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Barack Obama vs Mitt Romney. Epic Rap Battles Of History Season 2.',
            'liveBroadcastContent': 'none',
            'description': 'Download on iTunes ▻ http://hyperurl.co/Obama-vs-Romney ◅ Watch behind the scenes '
                           '▻ http://bit.ly/barackrom ◅ Check out our NEW Trump vs Clinton ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/dX_1B0w7Hzc/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/dX_1B0w7Hzc/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/dX_1B0w7Hzc/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/fawfYxmd23BJ72118LiJDA5Y9DA"',
        'id': {
            'videoId': 'dX_1B0w7Hzc',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2014-09-03T04:09:32.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Wheel of Musical Impressions with Adam Levine',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy challenges Adam to a friendly game of random musical impressions, like Michael'
                           ' Jackson singing the Sesame Street theme song. Subscribe NOW to The ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/zCbfWGgp9qs/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/zCbfWGgp9qs/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/zCbfWGgp9qs/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/wOPP5DcqJl9zSwSmHzf6cNBA0u0"',
        'id': {
            'videoId': 'zCbfWGgp9qs',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-06-14T08:47:57.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'James Bond vs Austin Powers - Epic Rap Battles of History - Season 5',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻http://hyperurl.co/Bond-vs-Powers◅ Watch the Behind the Scenes'
                           ' ▻http://bit.ly/BondvsPowers-BTS◅ Say Hi to Ben Atha (James Bond) ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/Iy7xDGi5lp4/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/Iy7xDGi5lp4/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/Iy7xDGi5lp4/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/in-gGD5NIiWtpuwdg0eDB6KbZN4"',
        'id': {
            'videoId': 'Iy7xDGi5lp4',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-02-04T05:21:45.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Wheel of Musical Impressions with Alessia Cara',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy challenges Alessia Cara to a game of random musical impressions like Ariana '
                           'Grande singing "Skidamarink" and Lorde singing "Baa, Baa, Black Sheep.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/2OFKM2G-dE8/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/2OFKM2G-dE8/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/2OFKM2G-dE8/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/qUpOosa41zzsEE2ir69gQ4BgS8Q"',
        'id': {
            'videoId': '2OFKM2G-dE8',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-01-07T04:55:46.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Jimmy Fallon\xa0Blew a Chance to Date Nicole Kidman',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy Fallon and Nicole Kidman have two very different embarrassing memories of the '
                           'afternoon they first met. Subscribe NOW to The Tonight Show Starring ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/qtsNbxgPngA/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/qtsNbxgPngA/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/qtsNbxgPngA/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/lDvXuGRVvbR-noPwpm-uv54Cg3U"',
        'id': {
            'videoId': 'qtsNbxgPngA',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-02-03T22:00:17.000Z',
            'channelId': 'UClVrJwcIy7saPcGc1nct80A',
            'title': 'twenty one pilots: Heavydirtysoul [OFFICIAL VIDEO]',
            'liveBroadcastContent': 'none',
            'description': "twenty one pilots' music video for 'Heavydirtysoul' from the album, Blurryface - "
                           "available now on Fueled By Ramen. Get it on… iTunes: ...",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/r_9Kf0D5BTs/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/r_9Kf0D5BTs/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/r_9Kf0D5BTs/default.jpg'
                }
            },
            'channelTitle': 'Fueled By Ramen'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/fxTNyIwcmEyGfT5g6Caf2B_MtaE"',
        'id': {
            'videoId': 'r_9Kf0D5BTs',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-09-01T09:00:01.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'The Stranger Things Kids Rehash That Kissing Scene',
            'liveBroadcastContent': 'none',
            'description': "Millie Bobby Brown and Finn Wolfhard have very different opinions about how bad the "
                           "kiss they shared turned out on the set of Netflix's Stranger Things.",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/AQt9tM3fWsY/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/AQt9tM3fWsY/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/AQt9tM3fWsY/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/b25jEVLL7rBpJ-5AdzOOoN04e20"',
        'id': {
            'videoId': 'AQt9tM3fWsY',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2013-11-18T14:00:06.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Bob Ross vs Pablo Picasso - Epic Rap Battles of History Season 3.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Ross-vs-Picasso ◅ Watch behind the scenes ▻ '
                           'http://bit.ly/rosspab ◅ "We don\'t make mistakes, just happy little ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/WGN5xaQkFk0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/WGN5xaQkFk0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/WGN5xaQkFk0/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/F_SEekT4c5cVQKq8MfIgRoe7v0M"',
        'id': {
            'videoId': 'WGN5xaQkFk0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-02-08T14:01:00.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': "'Finish the Lyric' with Ellen, James Corden & Jesse Tyler Ferguson",
            'liveBroadcastContent': 'none',
            'description': 'Ellen and the Grammy Awards host went head to head in this musical game, with the '
                           '"Modern Family" star as first-time host.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/Op0dL4mrmic/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/Op0dL4mrmic/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/Op0dL4mrmic/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/tuUnq0kQCVuftVtRDMcs6VuzCDk"',
        'id': {
            'videoId': 'Op0dL4mrmic',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-12-02T07:59:01.000Z',
            'channelId': 'UCJrOtniJ0-NWz37R30urifQ',
            'title': 'Alan Walker - Alone',
            'liveBroadcastContent': 'none',
            'description': 'Listen to ”Alone” on Spotify: http://bit.ly/AlanWalkerAlone Listen to ”Alone” via '
                           'other plattforms: https://alanwalker.lnk.to/Alone Merch available at ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/1-xGerv5FOk/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/1-xGerv5FOk/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/1-xGerv5FOk/default.jpg'
                }
            },
            'channelTitle': 'Alan Walker'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/FrTwzky9U2mIk0BetZiruvhFTE4"',
        'id': {
            'videoId': '1-xGerv5FOk',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-02-20T05:20:09.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Wheel of Musical Impressions with Demi Lovato',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy challenges Demi to a game of random musical impressions, such as Fetty Wap singing'
                           ' "Twinkle Twinkle Little Star." Subscribe NOW to The Tonight Show ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/GWpVTGnr_hA/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/GWpVTGnr_hA/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/GWpVTGnr_hA/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/-78NyvJe2YmOrTGg9-QI02X5fk0"',
        'id': {
            'videoId': 'GWpVTGnr_hA',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-09-16T04:17:29.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Wheel of Musical Impressions with Ariana Grande',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy challenges Ariana to a game of random musical impressions, such as Christina '
                           'Aguilera singing "The Wheels on the Bus." Subscribe NOW to The ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/ss9ygQqqL2Q/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/ss9ygQqqL2Q/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/ss9ygQqqL2Q/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/eOvbItTROIr600hbADetLTFIgPc"',
        'id': {
            'videoId': 'ss9ygQqqL2Q',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-13T14:01:00.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': 'A Too Cute 2-Year-Old Bottle Flipper!',
            'liveBroadcastContent': 'none',
            'description': "Sammy became an internet sensation after her bottle-flipping skills were posted "
                           "on Facebook, and now she's here to show Ellen how it's done. Prepare to meet ...",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/qsYUDM15T8U/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/qsYUDM15T8U/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/qsYUDM15T8U/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/UnTG73hRbTDo5fWPxYVjbslje4A"',
        'id': {
            'videoId': 'qsYUDM15T8U',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-06T04:59:03.000Z',
            'channelId': 'UC0C-w0YjGpqDXGB8IHb662A',
            'title': 'Ed Sheeran - Shape Of You [Official Lyric Video]',
            'liveBroadcastContent': 'none',
            'description': "Watch the official video now: https://www.youtube.com/watch?v=JGwWNGJdvx8 Stream "
                           "or Download Shape Of You: https://atlanti.cr/2singles Pre-order '÷'.",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/_dK2tDK9grQ/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/_dK2tDK9grQ/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/_dK2tDK9grQ/default.jpg'
                }
            },
            'channelTitle': 'Ed Sheeran'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/a26DNHcPlFBdQuip_CE73cSsvhY"',
        'id': {
            'videoId': '_dK2tDK9grQ',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-02-24T05:09:08.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Wheel of Musical Impressions with Christina Aguilera',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy challenges Christina to a game of random musical impressions, such as'
                           ' Britney Spears singing "This Little Piggy." Subscribe NOW to The Tonight Show ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/uD2nOjV3AaI/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/uD2nOjV3AaI/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/uD2nOjV3AaI/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/gNeNFlUvwfdbZ1eeSV2kI5NsVjE"',
        'id': {
            'videoId': 'uD2nOjV3AaI',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-09-14T13:00:01.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': 'Ellen and First Lady Michelle Obama Go to CVS',
            'liveBroadcastContent': 'none',
            'description': 'To help prepare the First Lady for life after the White House, Ellen took her to CVS '
                           'Pharmacy to pick up a few things.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/2ihOXaU0I8o/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/2ihOXaU0I8o/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/2ihOXaU0I8o/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/FzuICOo14RbnmuS6JzmTS9UVUS8"',
        'id': {
            'videoId': '2ihOXaU0I8o',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-05-18T08:12:09.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Gordon Ramsay vs Julia Child.  Epic Rap Battles of History - Season 5',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻ http://hyperurl.co/Ramsay-vs-Child ◅ Watch the Behind the Scenes '
                           '▻ https://youtu.be/8y5QN0xgDac ◅ Say Hi to Mamrie Hart: ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/99-n42Xb6NQ/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/99-n42Xb6NQ/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/99-n42Xb6NQ/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/WZ21sPCVYxFSBM5rbzdC0xpREa0"',
        'id': {
            'videoId': '99-n42Xb6NQ',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2015-05-05T03:58:02.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Jimmy Fallon & Jack Black Recreate "More Than Words" Music Video',
            'liveBroadcastContent': 'none',
            'description': 'Jimmy & Jack do a shot-for-shot remake of Extreme\'s "More Than Words" music video. '
                           'Subscribe NOW to The Tonight Show Starring Jimmy Fallon: ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/1ISYT6EeUM0/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/1ISYT6EeUM0/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/1ISYT6EeUM0/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/TqbO1gksXmPcOzDFu0lytacwwjI"',
        'id': {
            'videoId': '1ISYT6EeUM0',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-09-30T02:22:11.000Z',
            'channelId': 'UCi7GJNg51C3jgmYTUwqoUXA',
            'title': 'Conan Hits The Gym With Kevin Hart  - CONAN on TBS',
            'liveBroadcastContent': 'none',
            'description': 'Kevin and Conan work all the major muscle groups: biceps, lats, and of course, the '
                           'taint. "Kevin Hart: What Now?" is in theaters on October 14th.',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/jDdKtWnFXFo/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/jDdKtWnFXFo/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/jDdKtWnFXFo/default.jpg'
                }
            },
            'channelTitle': 'Team Coco'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/x542Z3WNKoSArhvnJOm4F_CAv5A"',
        'id': {
            'videoId': 'jDdKtWnFXFo',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-10T02:32:02.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Nice Peter vs EpicLLOYD - Epic Rap Battles of History Season Finale.',
            'liveBroadcastContent': 'none',
            'description': 'Download this song: http://hyperurl.co/NPvsEL_2 New ERB Swag is in! http://ERBMerch.com '
                           'Thank you to you. np & eL CAST ========= Nice Peter: Himself ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/0mbGUld2w-s/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/0mbGUld2w-s/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/0mbGUld2w-s/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/eY9m-5p9pj91Rdi_4MbP5WkeU0I"',
        'id': {
            'videoId': '0mbGUld2w-s',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-07-12T09:48:53.000Z',
            'channelId': 'UCMu5gPmKp5av0QCAajKTMhw',
            'title': 'Alexander the Great vs Ivan the Terrible - Epic Rap Battles of History Season 5',
            'liveBroadcastContent': 'none',
            'description': 'Download this song ▻http://hyperurl.co/Ivan-vs-the-Greats◅ Watch the Behind the Scenes'
                           ' ▻http://bit.ly/greatbts◅ Say hi to Meghan Tonjes ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/NVbH1BVXywY/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/NVbH1BVXywY/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/NVbH1BVXywY/default.jpg'
                }
            },
            'channelTitle': 'ERB'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/Lguj1EU1GgD7FEKEoVjBmL5wSQA"',
        'id': {
            'videoId': 'NVbH1BVXywY',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-30T10:57:50.000Z',
            'channelId': 'UC0C-w0YjGpqDXGB8IHb662A',
            'title': 'Ed Sheeran - Shape of You [Official Video]',
            'liveBroadcastContent': 'none',
            'description': "Stream or Download Shape Of You: https://atlanti.cr/2singles Pre-order '÷'. Out 3rd "
                           "March: https://atlanti.cr/yt-album Subscribe to Ed's channel: ...",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/JGwWNGJdvx8/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/JGwWNGJdvx8/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/JGwWNGJdvx8/default.jpg'
                }
            },
            'channelTitle': 'Ed Sheeran'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/iY8GqQkoAOsgSpcnKtKcbW5vlfk"',
        'id': {
            'videoId': 'JGwWNGJdvx8',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-18T14:01:30.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': "Mom of Quadruplets Talks Her Viral 'Mommy Break'",
            'liveBroadcastContent': 'none',
            'description': 'After the video she filmed while taking some "me time" in her pantry took the '
                           'Internet by storm, Ellen had to meet Ashley, her husband and their four little g'
                           'irls in ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/yEZKhfJSoNk/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/yEZKhfJSoNk/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/yEZKhfJSoNk/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/bjeBqY-_SBV6rYaiMfLkTQ5PY90"',
        'id': {
            'videoId': 'yEZKhfJSoNk',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-02-01T05:11:44.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': 'Mad Lib Theater with Dakota Johnson (Fifty Shades Darker Edition)',
            'liveBroadcastContent': 'none',
            'description': "Jimmy and Dakota Johnson perform an intense Fifty Shades Darker-inspired scene "
                           "they've written together using Mad Libs. Subscribe NOW to The Tonight ...",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/XHce62IrMOQ/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/XHce62IrMOQ/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/XHce62IrMOQ/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/3WDPuPXNEVjl3EmDAYpGt1MU98M"',
        'id': {
            'videoId': 'XHce62IrMOQ',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-09T02:08:36.000Z',
            'channelId': 'UC8-Th83bH_thdKZDJCrn88g',
            'title': "Jimmy Fallon's Golden Globes Cold Open",
            'liveBroadcastContent': 'none',
            'description': 'Host Jimmy Fallon kicks off the 74th Annual Golden Globe Awards. Subscribe NOW to '
                           'The Tonight Show Starring Jimmy Fallon: http://bit.ly/1nwT1aN Watch The ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/XaldSt0lc8o/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/XaldSt0lc8o/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/XaldSt0lc8o/default.jpg'
                }
            },
            'channelTitle': 'The Tonight Show Starring Jimmy Fallon'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/y2CINlsUTrVzZ8sIAsNYulngXXg"',
        'id': {
            'videoId': 'XaldSt0lc8o',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2017-01-19T16:01:30.000Z',
            'channelId': 'UCp0hYYBW6IMayGgR-WeoCvQ',
            'title': "Ellen's Tribute to the Obamas",
            'liveBroadcastContent': 'none',
            'description': "To commemorate President Obama's last day in office, Ellen took a look back at some"
                           " of her favorite moments with President Obama and the First Lady.",
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/dCsr0CNqB3g/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/dCsr0CNqB3g/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/dCsr0CNqB3g/default.jpg'
                }
            },
            'channelTitle': 'TheEllenShow'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/5BtIZdzuBzFOvhiMRcS42kDLZOo"',
        'id': {
            'videoId': 'dCsr0CNqB3g',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-06-30T15:07:59.000Z',
            'channelId': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
            'title': 'TRY NOT TO CRINGE CHALLENGE 2 (w/ MARZIA)',
            'liveBroadcastContent': 'none',
            'description': 'Thanks for da like ☆~(◡﹏◕✿) PART 1 https://www.youtube.com/watch?v=TIq-307wiQk CHECK '
                           'OUT MY GIVEAWAY /W G2A: ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/QYOgmDr_-ZE/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/QYOgmDr_-ZE/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/QYOgmDr_-ZE/default.jpg'
                }
            },
            'channelTitle': 'PewDiePie'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/IgE0Cq5fMJL1lYJavHpqy8j2i8o"',
        'id': {
            'videoId': 'QYOgmDr_-ZE',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2012-04-09T10:39:16.000Z',
            'channelId': 'UCtinbF-Q-fVthA0qrFQTgXQ',
            'title': 'Make It Count',
            'liveBroadcastContent': 'none',
            'description': 'follow me on snapchat - caseyneistat check out my second channel - https://www.youtube'
                           '.com/snapstories on http://instagram.com/caseyneistat on ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/WxfZkMm3wcg/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/WxfZkMm3wcg/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/WxfZkMm3wcg/default.jpg'
                }
            },
            'channelTitle': 'CaseyNeistat'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/AC1JmRud7ectBRMS1x9VW6Zyjw4"',
        'id': {
            'videoId': 'WxfZkMm3wcg',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }, {
        'snippet': {
            'publishedAt': '2016-10-21T11:30:36.000Z',
            'channelId': 'UCvhQPdeTHzIRneScV8MIocg',
            'title': 'Clean Bandit - Rockabye ft. Sean Paul & Anne-Marie [Official Video]',
            'liveBroadcastContent': 'none',
            'description': 'Vote for us to win British Video at the BRITs! Just tweet #BritVidCleanBandit. Download '
                           'or stream now at: https://atlanti.cr/rockabye Here is the official video for ...',
            'thumbnails': {
                'high': {
                    'height': 360,
                    'width': 480,
                    'url': 'https://i.ytimg.com/vi/papuvlVeZg8/hqdefault.jpg'
                },
                'medium': {
                    'height': 180,
                    'width': 320,
                    'url': 'https://i.ytimg.com/vi/papuvlVeZg8/mqdefault.jpg'
                },
                'default': {
                    'height': 90,
                    'width': 120,
                    'url': 'https://i.ytimg.com/vi/papuvlVeZg8/default.jpg'
                }
            },
            'channelTitle': 'Clean Bandit'
        },
        'etag': '"uQc-MPTsstrHkQcRXL3IWLmeNsM/83HxkCPw__cShsf_ag1JEpNXhj8"',
        'id': {
            'videoId': 'papuvlVeZg8',
            'kind': 'youtube#video'
        },
        'kind': 'youtube#searchResult'
    }],
    'kind': 'youtube#searchListResponse'
}


RSS_FEED_RESPONSE_DATA = {'items': [{
    'summary_detail': {
        'value': '<img src="https://68.media.tumblr.com/a82f3228a9a7a6bf8f913a567bab25ca',
        'language': None,
        'base': '',
        'type': 'text/html'
    },
    'id': 'https://staff.tumblr.com/post/157331097080',
    'updated_parsed': (timezone.now() - timedelta(days=6)).timetuple(),
    'title_detail': {
        'value': 'Tumblr turns 10 years old this weekend! Here’s one way to...',
        'language': None,
        'base': '',
        'type': 'text/plain'
    },
    'link': 'https://staff.tumblr.com/post/157331097080',
    'links': [{
        'href': 'https://staff.tumblr.com/post/157331097080',
        'rel': 'alternate',
        'type': 'text/html'
    }],
    'summary': '<img src="https://68.media.tumblr.com/a82f3228a9a7a6bf8f913a567bab25ca/tumblr_olhgemMMqj1'
               'qz8q0ho',
               'published': 'Thu, 16 Feb 2017 17:51:40 -0500',
    'guidislink': False,
    'title': 'Tumblr turns 10 years old this weekend! Here’s one way to...',
    'tags': [{
        'label': None,
        'scheme': None,
        'term': 'answertime'
    }, {
        'label': None,
        'scheme': None,
        'term': 'whoa'
    }, {
        'label': None,
        'scheme': None,
        'term': 'maybe ask him something about motorcycles?'
    }, {
        'label': None,
        'scheme': None,
        'term': 'why not'
    }, {
        'label': None,
        'scheme': None,
        'term': 'you only live once'
    }, {
        'label': None,
        'scheme': None,
        'term': 'vroom vroom vroom'
    }, {
        'label': None,
        'scheme': None,
        'term': 'hbdtumblr'
    }]
}, {
    'summary_detail': {
        'value': '<img src="https://68.media.tumblr.com/7ba82b8a75654304a74c07b18fd6f65f/tumblr_olhgk9L',
        'language': None,
        'base': '',
        'type': 'text/html'
    },
    'id': 'https://staff.tumblr.com/post/157326208100',
    'updated_parsed': (timezone.now() - timedelta(days=6)).timetuple(),
    'title_detail': {
        'value': 'david:\n10 years ago this Sunday, with modest expectations and...',
        'language': None,
        'base': '',
        'type': 'text/plain'
    },
    'link': 'https://staff.tumblr.com/post/157326208100',
    'links': [{
        'href': 'https://staff.tumblr.com/post/157326208100',
        'rel': 'alternate',
        'type': 'text/html'
    }],
    'summary': '<img src="https://68.media.tumblr.com/7ba82b8a75654304a74c07b18fd6f65f/tumblr_olhgk9LNpV1qz4r',
    'published': 'Thu, 16 Feb 2017 15:33:18 -0500',
    'guidislink': False,
    'title': 'david:\n10 years ago this Sunday, with modest expectations and...',
    'tags': [{
        'label': None,
        'scheme': None,
        'term': 'hbdtumblr'
    }]
}, {
    'summary_detail': {
        'value': '<img src="https://68.media.tumblr.com/be9cd2a502d0ef857368f05d35667634/tumblr_olh9bl4EMU1qfskc8o1',
        'language': None,
        'base': '',
        'type': 'text/html'
    },
    'id': 'https://staff.tumblr.com/post/157321774630',
    'updated_parsed': (timezone.now() - timedelta(days=6)).timetuple(),
    'title_detail': {
        'value': 'thirteenwnet:\nTHIRTEEN’s The Talk – Race in America Tackles the...',
        'language': None,
        'base': '',
        'type': 'text/plain'
    },
    'link': 'https://staff.tumblr.com/post/157321774630',
    'links': [{
        'href': 'https://staff.tumblr.com/post/157321774630',
        'rel': 'alternate',
        'type': 'text/html'
    }],
    'summary': '<img src="https://68.media.tumblr.com/be9cd2a502d0ef857368f05d35667634/tumblr_olh9bl4EMU1qfskc8o1_',
               'published': 'Thu, 16 Feb 2017 13:14:57 -0500',
    'guidislink': False,
    'title': 'thirteenwnet:\nTHIRTEEN’s The Talk – Race in America Tackles the...',
    'tags': [{
        'label': None,
        'scheme': None,
        'term': 'black history month'
    }, {
        'label': None,
        'scheme': None,
        'term': 'takeaction'
    }]
}, {
    'summary_detail': {
        'value': '<img src="https://68.media.tumblr.com/9eb0aec2188b47c6223ff165f4ce6497/tumblr_olc9autpJj'
                 '1w0ry43o1_500.jpg"/><br/><br/><p><a href="https://i-am-a-fish.tumblr.com/post/157212083307/ext'
                 'ra-special-valentines-day-card" class="tumblr_blog">i-am-a-fish</a>:</p><blockquote><p>Extra s'
                 'pecial valentine’s day card</p></blockquote>',
        'language': None,
        'base': '',
        'type': 'text/html'
    },
    'id': 'https://staff.tumblr.com/post/157240555555',
    'updated_parsed': (timezone.now() - timedelta(days=6)).timetuple(),
    'title_detail': {
        'value': 'i-am-a-fish:Extra special valentine’s day card',
        'language': None,
        'base': '',
        'type': 'text/plain'
    },
    'link': 'https://staff.tumblr.com/post/157240555555',
    'links': [{
        'href': 'https://staff.tumblr.com/post/157240555555',
        'rel': 'alternate',
        'type': 'text/html'
    }],
    'summary': '<img src="https://68.media.tumblr.com/9eb0aec2188b47c6223ff165f4ce6497/tumblr_olc9autpJ'
               'j1w0ry43o1_500.jpg"/><br/><br/><p><a href="https://i-am-a-fish.tumblr.com/post/157212083307/'
               'extra-special-valentines-day-card" class="tumblr_blog">i-am-a-fish</a>:</p><blockquote><p>Extr'
               'a special valentine’s day card</p></blockquote>',
    'published': 'Tue, 14 Feb 2017 13:00:29 -0500',
    'guidislink': False,
    'title': 'i-am-a-fish:Extra special valentine’s day card',
    'tags': [{
        'label': None,
        'scheme': None,
        'term': 'i-am-a-fish is QUITE the account'
    }, {
        'label': None,
        'scheme': None,
        'term': "happy valentine's day"
    }]
}, {
    'summary_detail': {
        'value': '<iframe width="400" height="225"  id="youtube_iframe" src="https://www.youtube.com/embed/b',
        'language': None,
        'base': '',
        'type': 'text/html'
    },
    'id': 'https://staff.tumblr.com/post/157237943629',
    'updated_parsed': (timezone.now() - timedelta(days=6)).timetuple(),
    'title_detail': {
        'value': 'postitforward:\nHappy Valentine’s Day, Tumblr. 💖\nToday we’re...',
        'language': None,
        'base': '',
        'type': 'text/plain'
    },
    'link': 'https://staff.tumblr.com/post/157237943629',
    'links': [{
        'href': 'https://staff.tumblr.com/post/157237943629',
        'rel': 'alternate',
        'type': 'text/html'
    }],
    'summary': '<iframe width="400" height="225"  id="youtube_iframe" src="https://www.youtube.com/',
    'published': 'Tue, 14 Feb 2017 11:30:22 -0500',
    'guidislink': False,
    'title': 'postitforward:\nHappy Valentine’s Day, Tumblr. 💖\nToday we’re...'
}]}


UNSORTED_FEED_LIST = [{
    'timestamp': timezone.now() - timedelta(days=6),
    'title': 'Alan Walker - Alone'
}, {
    'timestamp': timezone.now() - timedelta(days=14),
    'title': 'Second title - Alone'
}, {
    'timestamp': timezone.now() - timedelta(days=2),
    'title': 'First title'
}]
