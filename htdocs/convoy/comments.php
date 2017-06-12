<hr>
<div class="commentform">
<div class="commenttitle">Report or correct variation information</div>
<div class="commentdesc">Fill out the form below and submit the information.</div><p>

<form method="post" action="/pages/comment.php" name="comment">
  Your Name:<br>
  <input type="text" name="myname" size="64"><p>
  Your E-Mail Address:<br>
  <input type="text" name="myemail" size="64"><p>
  <?php echo $subtitle; ?><br>
  <input type="radio" name="updatetype" value="Update">Update Variation Information<br>
  <input type="radio" name="updatetype" value="New">New Variation Report<br>
  <p>
  Please type the information you want to add below:<br>
  <textarea cols="60" rows="12" name="mycomment"></textarea></p>
<?php DoTextButtonSubmit("SUBMIT", "submit"); ?> -
<?php DoTextButtonReset('comment', 'reset'); ?>
  <input type="hidden" name="mysubject" value="<?php echo $subtitle; ?> Variation Report"></p>
</form>
</div>
<hr>
