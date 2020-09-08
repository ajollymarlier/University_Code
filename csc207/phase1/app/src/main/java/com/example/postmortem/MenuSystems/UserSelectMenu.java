package com.example.postmortem.MenuSystems;

import android.content.Intent;
import android.text.InputType;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.postmortem.GameManager;
import com.example.postmortem.User;
import com.example.postmortem.UserLoader;

import java.util.List;
import java.util.Optional;

class UserSelectMenu extends GameMenu {

    private final int USERNAME_BAR = 1;
    private final int PASSWORD_BAR = 2;

    UserSelectMenu(String title){
        super(title);
    }

    @Override
    public List<View> buildMenuItems(final AppCompatActivity context) {

        createMenuTitle(context);
        createUserFields(context);
        createButtons(context);

        return items;

    }

    private void createUserFields(AppCompatActivity context) {
        //set the properties of the username edittext
        EditText usernameBar = new EditText(context);
        usernameBar.setHint(EditText.AUTOFILL_HINT_NAME);
        usernameBar.setY(256);
        usernameBar.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        items.add(usernameBar);

        //set the properties of the password edittext
        EditText passwordBar = new EditText(context);
        passwordBar.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        passwordBar.setHint(EditText.AUTOFILL_HINT_PASSWORD);
        passwordBar.setY(384);
        passwordBar.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        items.add(passwordBar);
    }

    private void createMenuTitle(AppCompatActivity context) {
        //set the properties of the title
        TextView textView = new TextView(context);
        textView.setText(title);
        textView.setTextSize(32);
        textView.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
        textView.setY(64);
        textView.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        setColours(textView);
        items.add(textView);
    }

    private void createButtons(final AppCompatActivity context) {
        //set the properties of the login button
        Button loginButton = new Button(context);
        loginButton.setText("Login");
        loginButton.setTextSize(18);
        loginButton.setY(512);
        loginButton.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptLogin(context);
            }
        });
        setColours(loginButton);
        items.add(loginButton);

        //set the properties of the create user button
        Button createButton = new Button(context);
        createButton.setText("Create New User");
        createButton.setTextSize(18);
        createButton.setY(672);
        createButton.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        createButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptCreateAccount();
            }
        });
        setColours(createButton);
        items.add(createButton);
    }

    private void attemptLogin(AppCompatActivity context){

        Optional<User> user = getUserLoggedIn();
        if(user.isPresent()){
            loginSuccess(context, user.get());
        } else {
            loginFail();
        }
    }

    private Optional<User> getUserLoggedIn() {
        EditText usernameBar = (EditText) items.get(USERNAME_BAR);
        EditText passwordBar = (EditText) items.get(PASSWORD_BAR);

        String username = usernameBar.getText().toString();
        String password = passwordBar.getText().toString();

        return UserLoader.attemptLogin(username, password);
    }

    private void loginSuccess(AppCompatActivity context, User user){

        Intent oldIntent = context.getIntent();
        GameManager manager = oldIntent.getParcelableExtra("manager");

        Intent newIntent = GameMenu.openMenu(context, GameMenu.MAIN_MENU);
        manager.setActiveUser(user);
        newIntent.putExtra(GameManager.INTENT_NAME, manager);

        context.startActivity(newIntent);
        context.finish();

    }

    private void loginFail(){

        EditText usernameBar = (EditText) items.get(USERNAME_BAR);
        EditText passwordBar = (EditText) items.get(PASSWORD_BAR);

        usernameBar.setText("");
        usernameBar.setHint("Login failed, try  again");

        passwordBar.setText("");

    }

    private void attemptCreateAccount(){

        EditText usernameBar = (EditText) items.get(USERNAME_BAR);
        EditText passwordBar = (EditText) items.get(PASSWORD_BAR);

        String username = usernameBar.getText().toString();
        String password = passwordBar.getText().toString();

        boolean userCreated = UserLoader.createUser(username, password);

        if(userCreated){
            usernameBar.setHint("Account created");
            usernameBar.setText("");
            passwordBar.setText("");
            UserLoader.updateFiles();
        } else {
            usernameBar.setHint("Username Taken");
            usernameBar.setText("");
            passwordBar.setText("");
        }

    }

}
