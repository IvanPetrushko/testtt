<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{

    public function up(): void
    {
        Schema::table('phones', function (Blueprint $table) {
            $table->integer('memory');
            $table->integer('model');
        });
    }


    public function down(): void
    {
        Schema::table('phones', function (Blueprint $table) {
            $table->dropColumn('memory');
            $table->dropColumn('model');
        });
    }
};
