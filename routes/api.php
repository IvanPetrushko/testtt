<?php

use Illuminate\Support\Facades\Route;


//phone
Route::get('phones', [ \App\Http\Controllers\API\PhoneController::class, 'get' ]);
Route::post('phones/store', [ \App\Http\Controllers\API\PhoneController::class, 'store']);
Route::post('phones/store-from-raw', [ \App\Http\Controllers\API\PhoneController::class, 'storeFromRaw']);

//device
Route::get('device', [ \App\Http\Controllers\API\DeviceController::class, 'get']);
Route::post('device/store', [ \App\Http\Controllers\API\DeviceController::class, 'store']);
Route::post('device/store-from-raw', [ \App\Http\Controllers\API\DeviceController::class, 'storeFromRaw']);

//chats
Route::get('chats', [ \App\Http\Controllers\API\ChatController::class, 'get']);
Route::post('chats/store', [ \App\Http\Controllers\API\ChatController::class, 'store']);
Route::post('chats/update/{id}', [ \App\Http\Controllers\API\ChatController::class, 'update']);

//message
Route::get('message', [ \App\Http\Controllers\API\ChatMessageController::class, 'get']);
Route::post('message/store', [ \App\Http\Controllers\API\ChatMessageController::class, 'store']);
Route::post('message/delete-message/{id}', [ \App\Http\Controllers\API\ChatMessageController::class, 'deleteMessage']);
Route::post('message/delete-all-message/{id}', [ \App\Http\Controllers\API\ChatMessageController::class, 'deleteMessageByChat']);
