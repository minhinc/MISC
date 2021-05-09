<?php
function draw($util){
echo '<img style="max-width:100%" src="'.$util->level.'/image/election.png"/>
<script>
setInterval(function() {
                  window.location.reload();
                }, 300000); 
</script>';
}
?>
