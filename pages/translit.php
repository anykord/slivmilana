<?php
// translit.php — автоматически переводит кириллицу в транслит и редиректит 301

$old = $_GET['old'] ?? '';

// Твоя таблица соответствия (можно дополнять)
$translit = [
    'лизогуб-милана-слив-видео' => 'lizogub-milana-sliv-video',
    'слив-голых-фото-милана-хасетова' => 'sliv-golykh-foto-milana-khasetova',
    'слив-миланы-филимоновой-тг' => 'sliv-milany-filimonovoy-tg',
    '18-милана-хаметова-где-она-голая' => '18-milana-khametova-gde-ona-golaya',
    'секс-слив-миланы-некрасовой' => '18-seks-sliv-milana-nekrasova',
    // добавляй сюда все старые → новые имена
];

$new = $translit[$old] ?? str_replace([' ', 'ё'], ['-', 'yo'], strtolower(iconv('UTF-8', 'ASCII//TRANSLIT', $old)));

header("Location: /pages/{$new}.html", true, 301);
exit;
?>
