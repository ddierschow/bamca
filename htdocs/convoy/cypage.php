<?php if (!isset($argv)) { ?><!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
include "subs.php";
$pif = GetPageInfo("convoy");
$pif['title'] = $pif['title'] . ' - ' . $subtitle;
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

The Matchbox Convoy Project - <?php echo $subtitle; ?> - Under Construction<br>
<br>

<div class="title"><?php echo $subtitle; ?><br>
<?php echo $desc; ?>
</div>
<div class="description"><?php echo $year; ?></div>

<?php body(); ?>

<?php include "convoy/comments.php"; ?>
<br>
<div class="backlink">
<?php DoTextButtonLink('back', '/convoy/series.php'); ?> to the Convoy Index Page
</div>
</body>
</html><?php } ?>
