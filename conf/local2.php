<?php
/*
 * Dokuwiki's Main Configuration File - Local Settings 
 * Auto-generated by config plugin 
 * Run for user: admin
 * Date: Tue, 06 Jan 2009 22:44:06 +0100
 */

$conf['title'] = 'COmparing Continuous Optimisers: COCO';
$conf['template'] = 'arctic';
$conf['useacl'] = 1;
$conf['passcrypt'] = 'md5';
$conf['superuser'] = '@admin';
$conf['disableactions'] = 'register';
$conf['rss_linkto'] = 'current';
$conf['rss_content'] = 'htmldiff';
$conf['tpl']['arctic']['sidebar'] = 'right';
$conf['tpl']['arctic']['trace'] = 0;
$conf['tpl']['arctic']['left_sidebar_content'] = 'main,user,group,namespace,index';
$conf['tpl']['arctic']['right_sidebar_content'] = 'main,user,group,namespace,index';
$conf['tpl']['arctic']['search'] = 'right';

@include(DOKU_CONF.'local.protected.php');

// end auto-generated content
